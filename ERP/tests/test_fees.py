"""
Tests for fee collection workflow and receipt generation.
"""
import datetime
from decimal import Decimal

import pytest
from django.urls import reverse

from accounts.models import CustomUser
from fees.models import StudentFee, Payment
from .factories import (
    UserFactory, AccountantFactory,
    StudentFeeFactory, PaymentFactory, StudentFactory,
    FeeStructureFactory, FeeTypeFactory,
)

pytestmark = pytest.mark.django_db


@pytest.fixture
def accountant(db):
    return AccountantFactory()


@pytest.fixture
def admin(db):
    return UserFactory(role=CustomUser.ADMIN)


@pytest.fixture
def student_fee(db):
    return StudentFeeFactory(
        amount=Decimal('10000.00'),
        discount=Decimal('0.00'),
        net_amount=Decimal('10000.00'),
        status=StudentFee.UNPAID,
        due_date=datetime.date(2025, 10, 1),   # future — not overdue
    )


# ── Dashboard ─────────────────────────────────────────────────────────────────

class TestFeesDashboard:
    def test_dashboard_renders(self, client, accountant):
        client.force_login(accountant)
        resp = client.get(reverse('fees:dashboard'))
        assert resp.status_code == 200

    def test_teacher_denied_dashboard(self, client):
        teacher = UserFactory(role=CustomUser.TEACHER)
        client.force_login(teacher)
        resp = client.get(reverse('fees:dashboard'))
        assert resp.status_code in (302, 403)


# ── StudentFee model helpers ──────────────────────────────────────────────────

class TestStudentFeeModel:
    def test_balance_equals_net_when_no_payments(self, student_fee):
        assert student_fee.balance == student_fee.net_amount

    def test_balance_decreases_after_payment(self, student_fee, accountant):
        PaymentFactory(
            student_fee=student_fee,
            paid_amount=Decimal('3000.00'),
            collected_by=accountant,
        )
        student_fee.refresh_from_db()
        assert student_fee.balance == Decimal('7000.00')

    def test_status_becomes_paid_when_fully_settled(self, student_fee, accountant):
        PaymentFactory(
            student_fee=student_fee,
            paid_amount=Decimal('10000.00'),
            collected_by=accountant,
        )
        student_fee.refresh_status()
        assert student_fee.status == StudentFee.PAID

    def test_status_partial_on_partial_payment(self, student_fee, accountant):
        PaymentFactory(
            student_fee=student_fee,
            paid_amount=Decimal('4000.00'),
            collected_by=accountant,
        )
        student_fee.refresh_status()
        assert student_fee.status == StudentFee.PARTIAL

    def test_overdue_when_past_due_and_unpaid(self, db, accountant):
        fee = StudentFeeFactory(
            due_date=datetime.date(2023, 1, 1),
            status=StudentFee.UNPAID,
            net_amount=Decimal('5000.00'),
            amount=Decimal('5000.00'),
            discount=Decimal('0.00'),
        )
        fee.refresh_status()
        assert fee.status == StudentFee.OVERDUE


# ── Payment recording ─────────────────────────────────────────────────────────

class TestPaymentRecord:
    def test_payment_has_unique_receipt_number(self, db, accountant):
        sf1 = StudentFeeFactory()
        sf2 = StudentFeeFactory()
        p1  = PaymentFactory(student_fee=sf1, collected_by=accountant)
        p2  = PaymentFactory(student_fee=sf2, collected_by=accountant)
        assert p1.receipt_number != p2.receipt_number
        assert p1.receipt_number.startswith('RCP-')

    def test_payment_amount_clamped_to_balance(self, student_fee, accountant):
        # Paying more than balance should not create negative balance via view
        # (The view clamps it — test the model property directly)
        PaymentFactory(
            student_fee=student_fee,
            paid_amount=Decimal('10000.00'),      # exact balance
            collected_by=accountant,
        )
        assert student_fee.balance == Decimal('0.00')


# ── Receipt view ──────────────────────────────────────────────────────────────

class TestReceiptPrint:
    def test_receipt_renders_for_accountant(self, client, accountant, student_fee):
        payment = PaymentFactory(student_fee=student_fee, collected_by=accountant)
        client.force_login(accountant)
        resp = client.get(reverse('fees:receipt_print', kwargs={'payment_pk': payment.pk}))
        assert resp.status_code == 200
        assert payment.receipt_number.encode() in resp.content

    def test_receipt_404_for_missing_payment(self, client, accountant):
        client.force_login(accountant)
        resp = client.get(reverse('fees:receipt_print', kwargs={'payment_pk': 99999}))
        assert resp.status_code == 404

    def test_teacher_denied_receipt(self, client, student_fee, accountant):
        teacher = UserFactory(role=CustomUser.TEACHER)
        payment = PaymentFactory(student_fee=student_fee, collected_by=accountant)
        client.force_login(teacher)
        resp = client.get(reverse('fees:receipt_print', kwargs={'payment_pk': payment.pk}))
        assert resp.status_code in (302, 403)


# ── Outstanding view ──────────────────────────────────────────────────────────

class TestOutstandingReport:
    def test_outstanding_renders(self, client, accountant):
        client.force_login(accountant)
        resp = client.get(reverse('fees:outstanding'))
        assert resp.status_code == 200
