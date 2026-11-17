"""
Fee reminder emails — shared by the "Send reminders" button and the optional
nightly job. A family is never emailed more than once per
settings.FEE_REMINDER_COOLDOWN_DAYS, however many times either is triggered.
"""
from datetime import timedelta
from decimal import Decimal

from django.conf import settings
from django.core import mail
from django.utils import timezone

from .models import FeeReminderLog, StudentFee


def send_reminders(as_of=None, grade_id=None, division_id=None, user=None, automatic=False):
    as_of = as_of or timezone.localdate()
    fees = (StudentFee.objects.filter(due_date__lte=as_of)
            .exclude(status__in=['PAID', 'WAIVED'])
            .select_related('student', 'student__grade', 'fee_structure__fee_type'))
    if grade_id:
        fees = fees.filter(student__grade_id=grade_id)
    if division_id:
        fees = fees.filter(student__division_id=division_id)

    per_student = {}
    for f in fees:
        bal = f.balance
        if bal <= 0:
            continue
        entry = per_student.setdefault(f.student, {'total': Decimal('0'), 'lines': []})
        entry['total'] += bal
        entry['lines'].append(f"  - {f.fee_structure.fee_type.name}: SAR {bal:.2f} (due {f.due_date:%d %b %Y})")

    since = timezone.now() - timedelta(days=settings.FEE_REMINDER_COOLDOWN_DAYS)
    recently = set(FeeReminderLog.objects.filter(sent_at__gte=since).values_list('student_id', flat=True))

    sent = skipped = recent = failed = 0
    for stu, info in per_student.items():
        if stu.pk in recently:
            recent += 1
            continue
        email = stu.reminder_email()
        if not email:
            skipped += 1
            continue
        body = (
            f"Dear Parent,\n\n"
            f"This is a kind reminder from Al-Kawthar International School.\n"
            f"The following fees for {stu.full_name} ({stu.grade.name}) are outstanding:\n\n"
            + "\n".join(info['lines']) +
            f"\n\nTotal outstanding: SAR {info['total']:.2f}\n\n"
            f"Kindly arrange payment at your earliest convenience.\n"
            f"If you have already paid, please ignore this message.\n\n"
            f"Accounts Department\nAl-Kawthar International School"
        )
        try:
            mail.send_mail(
                subject=f"Fee Reminder — {stu.full_name} — SAR {info['total']:.2f} outstanding",
                message=body, from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email], fail_silently=False,
            )
        except Exception:                         # noqa: BLE001 — report, don't log: it will retry
            failed += 1
            continue
        FeeReminderLog.objects.create(student=stu, email=email, total=info['total'],
                                      automatic=automatic, sent_by=user)
        sent += 1

    msg = (f"{sent} reminder email(s) sent, {skipped} skipped (no parent email on file), "
           f"{recent} already reminded in the last {settings.FEE_REMINDER_COOLDOWN_DAYS} days.")
    if failed:
        msg += f" {failed} failed — check EMAIL_HOST settings in the environment."
    return {'ok': failed == 0, 'sent': sent, 'skipped': skipped, 'recent': recent,
            'failed': failed, 'message': msg}
