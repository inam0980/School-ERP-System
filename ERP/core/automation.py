"""
Nightly automation for the ERP — run by `python manage.py run_daily_jobs`
(scheduled by deploy/install_daily_jobs.bat).

Design rules:
- Everything runs locally; no student data is sent to any outside service.
- Every job is independent: one failure never stops the others, and failures
  are reported to the admins in the daily email.
- Nothing that contacts parents runs unless explicitly enabled in settings.
"""
import logging
import shutil
import sqlite3
from datetime import timedelta
from decimal import Decimal
from pathlib import Path

from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Sum
from django.utils import timezone

logger = logging.getLogger('erp.automation')

_DEFAULT = object()


# ════════════════════ BACKUP / RESTORE ════════════════════

def _sqlite_path():
    db = settings.DATABASES['default']
    if 'sqlite3' not in db['ENGINE']:
        return None
    return Path(db['NAME'])


def _integrity_ok(path):
    try:
        con = sqlite3.connect(f'file:{Path(path).as_posix()}?mode=ro', uri=True)
        try:
            return con.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
        finally:
            con.close()
    except sqlite3.DatabaseError:
        return False


def _sqlite_copy(source, target):
    """Consistent copy using SQLite's online-backup API (safe while the server is running)."""
    src = sqlite3.connect(f'file:{Path(source).as_posix()}?mode=ro', uri=True)
    dst = sqlite3.connect(str(target))
    try:
        src.backup(dst)
    finally:
        dst.close()
        src.close()


def _mirror(src_dir, dst_dir):
    """Copy new / changed files only. Never deletes from the backup."""
    copied = 0
    src_dir, dst_dir = Path(src_dir), Path(dst_dir)
    if not src_dir.is_dir():
        return 0
    for path in src_dir.rglob('*'):
        if not path.is_file():
            continue
        target = dst_dir / path.relative_to(src_dir)
        st = path.stat()
        if target.exists():
            tst = target.stat()
            if tst.st_size == st.st_size and int(tst.st_mtime) == int(st.st_mtime):
                continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
        copied += 1
    return copied


def backup_database(source=None, dest_dir=None, keep=None, media_dir=_DEFAULT):
    """
    Back up the SQLite database (verified with PRAGMA integrity_check) and mirror
    uploaded files. Keeps the newest `keep` database copies.
    Returns {'ok', 'message', 'file', 'media_copied'} — never raises for expected failures.
    """
    source = Path(source) if source else _sqlite_path()
    if source is None:
        return {'ok': False, 'message': 'Automatic backup supports SQLite only — use pg_dump for PostgreSQL.'}
    if not source.exists():
        return {'ok': False, 'message': f'Database file not found: {source}'}

    dest = Path(dest_dir or settings.BACKUP_DIR)
    dest.mkdir(parents=True, exist_ok=True)
    keep = keep or settings.BACKUP_KEEP

    stamp = timezone.localtime().strftime('%Y%m%d-%H%M%S')
    final = dest / f'erp-{stamp}.sqlite3'
    n = 1
    while final.exists():
        final = dest / f'erp-{stamp}-{n}.sqlite3'
        n += 1
    part = final.with_name(final.name + '.part')

    _sqlite_copy(source, part)
    if not _integrity_ok(part):
        part.unlink(missing_ok=True)
        return {'ok': False, 'message': 'Backup copy failed the integrity check — previous backups kept.'}
    part.replace(final)

    for old in sorted(dest.glob('erp-*.sqlite3'))[:-keep]:
        old.unlink(missing_ok=True)

    media_copied = 0
    if media_dir is _DEFAULT:
        media_dir = settings.MEDIA_ROOT
    if media_dir:
        media_copied = _mirror(media_dir, dest / 'media')

    size_mb = final.stat().st_size / 1024 / 1024
    msg = f'Backup OK: {final.name} ({size_mb:.1f} MB), {media_copied} uploaded file(s) copied.'
    logger.info(msg)
    return {'ok': True, 'message': msg, 'file': final, 'media_copied': media_copied}


def restore_database(backup_file, target=None):
    """
    Replace the live database with a verified backup. The current database is
    first saved as '<name>.before-restore-<time>.sqlite3' next to it.
    Stop the ERP service before restoring.
    """
    backup_file = Path(backup_file)
    target = Path(target) if target else _sqlite_path()
    if target is None:
        raise ValueError('Restore supports SQLite only.')
    if not backup_file.exists() or not _integrity_ok(backup_file):
        raise ValueError(f'{backup_file} is missing or not a valid, intact SQLite database.')

    stamp = timezone.localtime().strftime('%Y%m%d-%H%M%S')
    safety = target.with_name(f'{target.stem}.before-restore-{stamp}.sqlite3')
    if target.exists():
        _sqlite_copy(target, safety)
    _sqlite_copy(backup_file, target)
    if not _integrity_ok(target):
        raise ValueError(f'Restored database failed the integrity check — the previous one is at {safety}')
    logger.warning('Database restored from %s (previous copy: %s)', backup_file, safety)
    return {'ok': True, 'restored_from': backup_file, 'safety_copy': safety}


# ════════════════════ FEES ════════════════════

def refresh_fee_statuses():
    """
    A fee's status only changed when a payment was recorded, so a fee whose due
    date passed stayed UNPAID (and an OVERDUE fee whose due date was extended
    stayed OVERDUE). Re-evaluate those every night.
    """
    from fees.models import PaymentPlanInstallment, StudentFee
    today = timezone.localdate()

    fees_updated = 0
    stale = (StudentFee.objects.filter(status=StudentFee.UNPAID, due_date__lt=today) |
             StudentFee.objects.filter(status=StudentFee.OVERDUE, due_date__gte=today))
    for fee in stale.select_related('fee_structure__fee_type', 'student'):
        before = fee.status
        fee.refresh_status()
        fees_updated += fee.status != before

    inst_updated = 0
    stale_inst = (PaymentPlanInstallment.objects.filter(status=PaymentPlanInstallment.UNPAID, due_date__lt=today) |
                  PaymentPlanInstallment.objects.filter(status=PaymentPlanInstallment.OVERDUE, due_date__gte=today))
    for inst in stale_inst:
        before = inst.status
        inst.refresh_status()
        inst_updated += inst.status != before

    return {'ok': True, 'fees_updated': fees_updated, 'installments_updated': inst_updated,
            'message': f'{fees_updated} fee(s) and {inst_updated} installment(s) re-statused.'}


# ════════════════════ STAFF COMPLIANCE ════════════════════

IQAMA_WARNING_DAYS = 90
MOE_WARNING_DAYS = 60


def compliance_alerts():
    from staff.models import MOEApproval, StaffProfile
    today = timezone.localdate()
    iqamas = list(StaffProfile.objects.select_related('user')
                  .filter(iqama_expiry__isnull=False, user__is_active=True,
                          iqama_expiry__lte=today + timedelta(days=IQAMA_WARNING_DAYS))
                  .order_by('iqama_expiry'))
    moe = list(MOEApproval.objects.select_related('staff')
               .filter(status=MOEApproval.APPROVED, expiry_date__isnull=False,
                       expiry_date__lte=today + timedelta(days=MOE_WARNING_DAYS))
               .order_by('expiry_date'))
    return {'ok': True, 'iqamas': iqamas, 'moe': moe,
            'message': f'{len(iqamas)} Iqama(s) and {len(moe)} MOE document(s) expiring soon.'}


# ════════════════════ DAILY ADMIN EMAIL ════════════════════

def _digest_recipients():
    configured = getattr(settings, 'DIGEST_RECIPIENTS', [])
    if configured:
        return list(configured)
    from accounts.models import CustomUser
    return sorted(set(CustomUser.objects.filter(
        role__in=[CustomUser.SUPER_ADMIN, CustomUser.ADMIN], is_active=True,
    ).exclude(email='').values_list('email', flat=True)))


def send_daily_digest(results):
    """Internal summary for school admins (no parent contact)."""
    from fees.models import Payment, StudentFee

    recipients = _digest_recipients()
    if not recipients:
        return {'ok': True, 'message': 'No admin email on file — digest not sent.'}

    today = timezone.localdate()
    yday = today - timedelta(days=1)
    day = Payment.objects.filter(payment_date=yday)
    live = day.filter(is_voided=False).aggregate(s=Sum('paid_amount'))['s'] or Decimal('0')
    live_n = day.filter(is_voided=False).count()
    void_n = day.filter(is_voided=True).count()
    overdue = StudentFee.objects.filter(status=StudentFee.OVERDUE)
    overdue_total = overdue.aggregate(s=Sum('net_amount'))['s'] or Decimal('0')

    lines = [f'Al-Kawthar ERP — daily report for {today:%A %d %B %Y}', '',
             f'Collections on {yday:%d %b}: SAR {live:,.2f} ({live_n} receipt(s))',
             f'Voided receipts on {yday:%d %b}: {void_n}',
             f'Overdue fees now: {overdue.count()} (SAR {overdue_total:,.2f} billed)', '']

    comp = results.get('compliance') or {}
    if comp.get('iqamas') or comp.get('moe'):
        lines.append('Staff documents expiring soon:')
        for p in comp.get('iqamas', []):
            lines.append(f'  - Iqama: {p.user.full_name} ({p.employee_id}) — {p.iqama_expiry:%d %b %Y}')
        for m in comp.get('moe', []):
            lines.append(f'  - {m.get_approval_type_display()}: {m.staff.full_name} — {m.expiry_date:%d %b %Y}')
        lines.append('')

    lines.append('Automated jobs:')
    failed = False
    for name, r in results.items():
        if name == 'digest':
            continue
        ok = r.get('ok', False)
        failed |= not ok
        lines.append(f"  [{'OK' if ok else 'FAILED'}] {name}: {r.get('message', '')}")

    subject = f"{'⚠ ' if failed else ''}ERP daily report — {today:%d %b %Y}"
    send_mail(subject, '\n'.join(lines), settings.DEFAULT_FROM_EMAIL, recipients, fail_silently=False)
    return {'ok': True, 'message': f'Sent to {len(recipients)} admin(s).'}


# ════════════════════ RUNNER ════════════════════

def _safe(name, fn, results):
    try:
        out = fn() or {}
        out.setdefault('ok', True)
    except Exception as exc:                       # noqa: BLE001 — one job must never stop the rest
        logger.exception('Daily job %s failed', name)
        out = {'ok': False, 'message': f'{type(exc).__name__}: {exc}'}
    results[name] = out
    return out


def run_daily_jobs():
    results = {}
    _safe('backup', lambda: backup_database(), results)
    _safe('fee_statuses', refresh_fee_statuses, results)
    _safe('compliance', compliance_alerts, results)
    if getattr(settings, 'AUTO_FEE_REMINDERS', False):
        from fees.reminders import send_reminders
        _safe('fee_reminders', lambda: send_reminders(automatic=True), results)
    _safe('digest', lambda: send_daily_digest(results), results)
    return results
