"""
Nightly automation (core/automation.py) — everything runs locally; nothing
sends student data outside the school server.
"""
import datetime
import sqlite3
from decimal import Decimal as D

import pytest
from django.core import mail

from core import automation
from fees.models import PaymentPlanInstallment, StudentFee
from tests import factories as f

TODAY = datetime.date.today()


# ── Backup ───────────────────────────────────────────────────────────────────

def _make_db(path, rows=3):
    con = sqlite3.connect(path)
    con.execute('CREATE TABLE t (id INTEGER PRIMARY KEY, v TEXT)')
    con.executemany('INSERT INTO t (v) VALUES (?)', [(f'r{i}',) for i in range(rows)])
    con.commit()
    con.close()


class TestBackupDatabase:
    def test_creates_verified_copy(self, tmp_path):
        src = tmp_path / 'db.sqlite3'
        _make_db(src)
        result = automation.backup_database(source=src, dest_dir=tmp_path / 'backups', media_dir=None)
        assert result['ok'] and result['file'].exists()
        con = sqlite3.connect(result['file'])
        assert con.execute('SELECT COUNT(*) FROM t').fetchone()[0] == 3
        con.close()

    def test_keeps_only_newest_n(self, tmp_path):
        src = tmp_path / 'db.sqlite3'
        _make_db(src)
        dest = tmp_path / 'backups'
        dest.mkdir()
        for i in range(5):                                   # older backups
            (dest / f'erp-2020010{i}-000000.sqlite3').write_bytes(b'old')
        automation.backup_database(source=src, dest_dir=dest, keep=3, media_dir=None)
        kept = sorted(p.name for p in dest.glob('erp-*.sqlite3'))
        assert len(kept) == 3 and kept[-1] > 'erp-2020'     # newest survives
        assert 'erp-20200100-000000.sqlite3' not in kept

    def test_source_is_untouched(self, tmp_path):
        src = tmp_path / 'db.sqlite3'
        _make_db(src)
        before = src.read_bytes()
        automation.backup_database(source=src, dest_dir=tmp_path / 'b', media_dir=None)
        assert src.read_bytes() == before

    def test_missing_source_reports_failure_instead_of_crashing(self, tmp_path):
        result = automation.backup_database(source=tmp_path / 'nope.sqlite3', dest_dir=tmp_path / 'b', media_dir=None)
        assert result['ok'] is False and 'not found' in result['message'].lower()

    def test_mirrors_uploaded_files(self, tmp_path):
        src = tmp_path / 'db.sqlite3'
        _make_db(src)
        media = tmp_path / 'media' / 'students' / 'photos'
        media.mkdir(parents=True)
        (media / 'a.png').write_bytes(b'png-bytes')
        dest = tmp_path / 'backups'
        result = automation.backup_database(source=src, dest_dir=dest, media_dir=tmp_path / 'media')
        assert (dest / 'media' / 'students' / 'photos' / 'a.png').read_bytes() == b'png-bytes'
        assert result['media_copied'] == 1
        again = automation.backup_database(source=src, dest_dir=dest, media_dir=tmp_path / 'media')
        assert again['media_copied'] == 0                   # unchanged files are not re-copied


class TestRestoreDatabase:
    def test_restore_replaces_target_and_keeps_safety_copy(self, tmp_path):
        live = tmp_path / 'db.sqlite3'
        _make_db(live, rows=1)
        backup = tmp_path / 'good.sqlite3'
        _make_db(backup, rows=7)
        result = automation.restore_database(backup, target=live)
        con = sqlite3.connect(live)
        assert con.execute('SELECT COUNT(*) FROM t').fetchone()[0] == 7
        con.close()
        assert result['safety_copy'].exists()                # the replaced DB was kept

    def test_refuses_corrupt_backup(self, tmp_path):
        live = tmp_path / 'db.sqlite3'
        _make_db(live, rows=1)
        bad = tmp_path / 'bad.sqlite3'
        bad.write_bytes(b'this is not a database')
        with pytest.raises(ValueError):
            automation.restore_database(bad, target=live)
        con = sqlite3.connect(live)
        assert con.execute('SELECT COUNT(*) FROM t').fetchone()[0] == 1      # untouched
        con.close()


# ── Fee statuses ─────────────────────────────────────────────────────────────

@pytest.mark.django_db
class TestRefreshFeeStatuses:
    def test_unpaid_fee_past_due_becomes_overdue(self):
        fee = f.StudentFeeFactory(due_date=TODAY + datetime.timedelta(days=3))
        StudentFee.objects.filter(pk=fee.pk).update(due_date=TODAY - datetime.timedelta(days=1))
        result = automation.refresh_fee_statuses()
        fee.refresh_from_db()
        assert fee.status == StudentFee.OVERDUE and result['fees_updated'] == 1

    def test_partial_paid_and_waived_untouched(self):
        past = TODAY - datetime.timedelta(days=5)
        partial = f.StudentFeeFactory(amount=D('100'))
        f.PaymentFactory(student_fee=partial, paid_amount=D('10'))
        waived = f.StudentFeeFactory(status=StudentFee.WAIVED)
        StudentFee.objects.filter(pk__in=[partial.pk, waived.pk]).update(due_date=past)
        automation.refresh_fee_statuses()
        partial.refresh_from_db(); waived.refresh_from_db()
        assert partial.status == StudentFee.PARTIAL and waived.status == StudentFee.WAIVED

    def test_future_fee_stays_unpaid(self):
        fee = f.StudentFeeFactory(due_date=TODAY + datetime.timedelta(days=1))
        automation.refresh_fee_statuses()
        fee.refresh_from_db()
        assert fee.status == StudentFee.UNPAID

    def test_installments_past_due_become_overdue(self):
        inst = f.PaymentPlanInstallmentFactory(due_date=TODAY + datetime.timedelta(days=2))
        PaymentPlanInstallment.objects.filter(pk=inst.pk).update(due_date=TODAY - datetime.timedelta(days=1))
        automation.refresh_fee_statuses()
        inst.refresh_from_db()
        assert inst.status == PaymentPlanInstallment.OVERDUE


# ── Compliance ───────────────────────────────────────────────────────────────

@pytest.mark.django_db
class TestComplianceAlerts:
    def test_lists_expiring_iqamas_and_moe_documents(self):
        soon = f.StaffProfileFactory(iqama_expiry=TODAY + datetime.timedelta(days=30))
        f.StaffProfileFactory(iqama_expiry=TODAY + datetime.timedelta(days=200))
        expired = f.StaffProfileFactory(iqama_expiry=TODAY - datetime.timedelta(days=3))
        moe = f.MOEApprovalFactory(status='APPROVED', expiry_date=TODAY + datetime.timedelta(days=20))
        f.MOEApprovalFactory(status='APPROVED', expiry_date=TODAY + datetime.timedelta(days=120))
        result = automation.compliance_alerts()
        assert {p.pk for p in result['iqamas']} == {soon.pk, expired.pk}
        assert [m.pk for m in result['moe']] == [moe.pk]


# ── Daily digest & runner ────────────────────────────────────────────────────

@pytest.mark.django_db
class TestDailyDigest:
    def test_sent_to_active_admins_with_email(self):
        f.UserFactory(role='ADMIN', email='head@school.sa')
        f.SuperAdminFactory(email='owner@school.sa')
        f.UserFactory(role='ADMIN', email='gone@school.sa', is_active=False)
        f.TeacherFactory(email='teacher@school.sa')
        automation.send_daily_digest({'backup': {'ok': True, 'message': 'Backup OK'}})
        assert len(mail.outbox) == 1
        assert sorted(mail.outbox[0].to) == ['head@school.sa', 'owner@school.sa']

    def test_contains_yesterdays_collection_and_job_failures(self):
        f.UserFactory(role='ADMIN', email='head@school.sa')
        yday = TODAY - datetime.timedelta(days=1)
        f.PaymentFactory(paid_amount=D('750'), payment_date=yday)
        f.PaymentFactory(paid_amount=D('999'), payment_date=yday, is_voided=True)
        automation.send_daily_digest({'backup': {'ok': False, 'message': 'disk full'}})
        body = mail.outbox[0].body
        assert 'SAR 750.00' in body and '999' not in body.split('Voided')[0]
        assert 'FAILED' in body and 'disk full' in body
        assert '⚠' in mail.outbox[0].subject

    def test_no_admin_email_means_no_mail(self):
        automation.send_daily_digest({})
        assert mail.outbox == []


@pytest.mark.django_db
class TestRunDailyJobs:
    def test_one_failing_job_does_not_stop_the_others(self, monkeypatch, tmp_path):
        f.UserFactory(role='ADMIN', email='head@school.sa')
        monkeypatch.setattr(automation, 'backup_database', lambda **k: 1 / 0)
        fee = f.StudentFeeFactory(due_date=TODAY + datetime.timedelta(days=3))
        StudentFee.objects.filter(pk=fee.pk).update(due_date=TODAY - datetime.timedelta(days=1))
        results = automation.run_daily_jobs()
        assert results['backup']['ok'] is False and 'ZeroDivisionError' in results['backup']['message']
        fee.refresh_from_db()
        assert fee.status == StudentFee.OVERDUE                       # later job still ran
        assert 'FAILED' in mail.outbox[0].body                         # and admins are told

    def test_management_command(self, monkeypatch):
        from django.core.management import call_command
        monkeypatch.setattr(automation, 'backup_database', lambda **k: {'ok': True, 'message': 'skipped in test'})
        call_command('run_daily_jobs')
