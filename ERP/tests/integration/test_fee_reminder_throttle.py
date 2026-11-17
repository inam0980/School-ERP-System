"""
Fee reminders must never spam a family: one reminder per cooldown window
(default 7 days), whether sent by the button or by the optional nightly job.
"""
import datetime
from decimal import Decimal as D

import pytest
from django.urls import reverse
from django.utils import timezone

from tests import factories as f

pytestmark = pytest.mark.django_db


@pytest.fixture
def defaulter(school):
    school.student.father_email = 'father@example.com'
    school.student.save()
    f.StudentFeeFactory(student=school.student, amount=D('900'),
                        due_date=datetime.date.today() - datetime.timedelta(days=10))
    return school.student


def _click(client):
    return client.post(reverse('fees:send_reminders'), follow=True)


class TestReminderThrottle:
    def test_double_click_sends_only_once(self, login, accountant, defaulter, mailoutbox):
        client = login(accountant)
        _click(client)
        resp = _click(client)
        assert len(mailoutbox) == 1
        assert 'already reminded' in resp.content.decode()

    def test_sent_reminder_is_logged(self, login, accountant, defaulter, mailoutbox):
        from fees.models import FeeReminderLog
        _click(login(accountant))
        log = FeeReminderLog.objects.get()
        assert (log.student, log.email, log.total, log.automatic, log.sent_by) == \
               (defaulter, 'father@example.com', D('900.00'), False, accountant)

    def test_reminds_again_after_cooldown(self, login, accountant, defaulter, mailoutbox, settings):
        from fees.models import FeeReminderLog
        client = login(accountant)
        _click(client)
        FeeReminderLog.objects.update(
            sent_at=timezone.now() - datetime.timedelta(days=settings.FEE_REMINDER_COOLDOWN_DAYS, minutes=1))
        _click(client)
        assert len(mailoutbox) == 2

    def test_failed_send_is_not_logged_so_it_retries(self, login, accountant, defaulter, monkeypatch):
        from fees.models import FeeReminderLog

        def boom(*a, **k):
            raise ConnectionRefusedError('smtp down')
        monkeypatch.setattr('django.core.mail.send_mail', boom)
        _click(login(accountant))
        assert not FeeReminderLog.objects.exists()


class TestAutomaticReminders:
    def test_off_by_default(self, defaulter, mailoutbox, monkeypatch):
        from core import automation
        monkeypatch.setattr(automation, 'backup_database', lambda **k: {'ok': True, 'message': 'x'})
        results = automation.run_daily_jobs()
        assert 'fee_reminders' not in results
        assert [m for m in mailoutbox if 'Fee Reminder' in m.subject] == []

    def test_when_enabled_sends_once_per_cooldown(self, defaulter, mailoutbox, monkeypatch, settings):
        from core import automation
        from fees.models import FeeReminderLog
        settings.AUTO_FEE_REMINDERS = True
        monkeypatch.setattr(automation, 'backup_database', lambda **k: {'ok': True, 'message': 'x'})
        automation.run_daily_jobs()
        automation.run_daily_jobs()                       # next night: still within cooldown
        reminders = [m for m in mailoutbox if 'Fee Reminder' in m.subject]
        assert len(reminders) == 1
        assert FeeReminderLog.objects.get().automatic is True
