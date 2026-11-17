"""
Unit tests for fees/models.py — every money calculation in the system.

These pin the financial rules (VAT, discounts, refunds, voids, installments,
payroll) so a refactor can never silently change what a parent is charged.
"""
import datetime
from decimal import Decimal as D

import pytest

from fees.models import (
    FeeType, StudentFee, PaymentPlanInstallment, TuitionInstallment,
)
from tests import factories as f

pytestmark = pytest.mark.django_db

TODAY = datetime.date.today()


def _fee(student=None, amount='10000.00', discount='0.00', taxable=False, **kw):
    fee_type = f.TaxableFeeTypeFactory() if taxable else f.FeeTypeFactory()
    item = f.FeeStructureItemFactory(fee_type=fee_type, amount=D(amount))
    return f.StudentFeeFactory(
        student=student or f.StudentFactory(),
        fee_structure=item, amount=D(amount), discount=D(discount), **kw,
    )


# ── FeeType.vat_rate_for ─────────────────────────────────────────────────────

class TestVatRate:
    @pytest.mark.parametrize("taxable, is_saudi, expected", [
        (False, True,  D('0')),     # non-taxable fee, Saudi
        (False, False, D('0')),     # non-taxable fee, expat
        (True,  True,  D('0')),     # taxable but Saudi → MoE exemption
        (True,  False, D('0.15')),  # taxable and expat → 15%
    ])
    def test_vat_matrix(self, taxable, is_saudi, expected):
        ft = FeeType(name='X', is_taxable=taxable)
        assert ft.vat_rate_for(is_saudi) == expected


class TestFeeStructureItemVat:
    def test_expat_vat_on_taxable_item(self):
        item = f.FeeStructureItemFactory(fee_type=f.TaxableFeeTypeFactory(), amount=D('1000.00'))
        assert item.expat_vat == D('150.00')
        assert item.expat_total == D('1150.00')

    def test_no_vat_on_non_taxable_item(self):
        item = f.FeeStructureItemFactory(amount=D('1000.00'))
        assert item.expat_vat == D('0.00')
        assert item.expat_total == D('1000.00')


# ── StudentFee.save → net_amount ─────────────────────────────────────────────

class TestStudentFeeNetAmount:
    def test_saudi_pays_no_vat_even_on_taxable_fee(self):
        fee = _fee(student=f.StudentFactory(), taxable=True)
        assert fee.net_amount == D('10000.00')

    def test_expat_pays_15pct_vat_on_taxable_fee(self):
        fee = _fee(student=f.ExpatStudentFactory(), taxable=True)
        assert fee.net_amount == D('11500.00')

    def test_expat_pays_no_vat_on_non_taxable_fee(self):
        fee = _fee(student=f.ExpatStudentFactory(), taxable=False)
        assert fee.net_amount == D('10000.00')

    def test_vat_applies_after_discount(self):
        fee = _fee(student=f.ExpatStudentFactory(), taxable=True,
                   amount='1000.00', discount='200.00')
        assert fee.net_amount == D('920.00')     # (1000 − 200) × 1.15

    def test_discount_larger_than_amount_floors_at_zero(self):
        fee = _fee(amount='500.00', discount='800.00')
        assert fee.net_amount == D('0.00')

    def test_net_amount_passed_in_is_ignored_and_recomputed(self):
        fee = _fee(amount='1000.00', net_amount=D('1.00'))
        assert fee.net_amount == D('1000.00')

    def test_net_amount_rounded_to_halalas(self):
        fee = _fee(student=f.ExpatStudentFactory(), taxable=True, amount='333.33')
        assert fee.net_amount == D('383.33')     # 333.33 × 1.15 = 383.3295


# ── amount_paid / balance (voids & refunds) ──────────────────────────────────

class TestStudentFeeAmountPaid:
    def test_no_payments(self):
        fee = _fee()
        assert fee.amount_paid == D('0.00')
        assert fee.balance == D('10000.00')

    def test_payments_are_summed(self):
        fee = _fee()
        f.PaymentFactory(student_fee=fee, paid_amount=D('3000'))
        f.PaymentFactory(student_fee=fee, paid_amount=D('2000'))
        assert fee.amount_paid == D('5000')
        assert fee.balance == D('5000')

    def test_voided_payment_is_excluded(self):
        fee = _fee()
        f.PaymentFactory(student_fee=fee, paid_amount=D('3000'))
        f.PaymentFactory(student_fee=fee, paid_amount=D('2000'), is_voided=True)
        assert fee.amount_paid == D('3000')

    def test_refund_reduces_amount_paid(self):
        fee = _fee()
        p = f.PaymentFactory(student_fee=fee, paid_amount=D('3000'))
        f.RefundFactory(payment=p, amount=D('500'))
        assert fee.amount_paid == D('2500')
        assert fee.balance == D('7500')

    def test_other_students_payments_do_not_leak_in(self):
        fee, other = _fee(), _fee()
        f.PaymentFactory(student_fee=other, paid_amount=D('9999'))
        assert fee.amount_paid == D('0.00')


# ── refresh_status ───────────────────────────────────────────────────────────

class TestStudentFeeStatus:
    def test_unpaid_when_nothing_paid_and_not_due(self):
        fee = _fee(due_date=TODAY + datetime.timedelta(days=1))
        fee.refresh_status()
        assert fee.status == StudentFee.UNPAID

    def test_overdue_when_nothing_paid_and_past_due(self):
        fee = _fee(due_date=TODAY - datetime.timedelta(days=1))
        fee.refresh_status()
        assert fee.status == StudentFee.OVERDUE

    def test_not_overdue_on_due_date_itself(self):
        fee = _fee(due_date=TODAY)
        fee.refresh_status()
        assert fee.status == StudentFee.UNPAID

    def test_partial(self):
        fee = _fee()
        f.PaymentFactory(student_fee=fee, paid_amount=D('1'))
        fee.refresh_from_db()
        assert fee.status == StudentFee.PARTIAL

    def test_paid_when_fully_settled(self):
        fee = _fee()
        f.PaymentFactory(student_fee=fee, paid_amount=D('10000.00'))
        fee.refresh_from_db()
        assert fee.status == StudentFee.PAID

    def test_waived_is_never_overwritten(self):
        fee = _fee(status=StudentFee.WAIVED)
        f.PaymentFactory(student_fee=fee, paid_amount=D('10000.00'))
        fee.refresh_from_db()
        assert fee.status == StudentFee.WAIVED

    def test_full_refund_reverts_paid_to_unpaid(self):
        fee = _fee()
        p = f.PaymentFactory(student_fee=fee, paid_amount=D('10000.00'))
        f.RefundFactory(payment=p, amount=D('10000.00'))
        fee.refresh_status()
        assert fee.status == StudentFee.UNPAID

    def test_payment_save_triggers_status_refresh(self):
        """Payment.save() must update the parent fee without an explicit call."""
        fee = _fee()
        f.PaymentFactory(student_fee=fee, paid_amount=D('4000'))
        assert StudentFee.objects.get(pk=fee.pk).status == StudentFee.PARTIAL


# ── Payment / Refund ─────────────────────────────────────────────────────────

class TestPayment:
    def test_receipt_number_format_and_uniqueness(self):
        a, b = f.PaymentFactory(), f.PaymentFactory()
        assert a.receipt_number.startswith('RCP-')
        assert a.receipt_number != b.receipt_number

    def test_refundable_amount(self):
        p = f.PaymentFactory(paid_amount=D('1000'))
        f.RefundFactory(payment=p, amount=D('300'))
        f.RefundFactory(payment=p, amount=D('200'))
        assert p.refunded_amount == D('500')
        assert p.refundable_amount == D('500')

    def test_voided_payment_is_not_refundable(self):
        p = f.PaymentFactory(paid_amount=D('1000'), is_voided=True)
        assert p.refundable_amount == D('0.00')

    def test_refund_number_format(self):
        assert f.RefundFactory().refund_number.startswith('RFD-')


# ── Salary ───────────────────────────────────────────────────────────────────

class TestSalary:
    def test_net_salary_is_basic_plus_allowances_minus_deductions(self):
        s = f.SalaryFactory(basic=D('8000'), housing=D('2000'), transport=D('500'),
                            other_allowances=D('250'), deductions=D('1000'))
        assert s.net_salary == D('9750')

    def test_net_salary_never_negative(self):
        s = f.SalaryFactory(basic=D('1000'), deductions=D('5000'))
        assert s.net_salary == D('0.00')

    def test_net_salary_recomputed_on_every_save(self):
        s = f.SalaryFactory(basic=D('8000'))
        s.deductions = D('500')
        s.save()
        assert s.net_salary == D('7500')


# ── TuitionFeeConfig ─────────────────────────────────────────────────────────

class TestTuitionFeeConfig:
    def test_without_group_discount(self):
        c = f.TuitionFeeConfigFactory(gross_tuition_fee=D('20000'))
        assert c.group_discount_amount == D('0.00')
        assert c.net_tuition_fee == D('20000.00')
        assert c.vat_amount_non_saudi == D('3000.00')
        assert c.final_net_non_saudi == D('23000.00')

    def test_group_discount_only_when_enabled(self):
        c = f.TuitionFeeConfigFactory(gross_tuition_fee=D('20000'),
                                      group_discount_enabled=False, group_discount_pct=D('10'))
        assert c.group_discount_amount == D('0.00')

    def test_with_group_discount(self):
        c = f.TuitionFeeConfigFactory(gross_tuition_fee=D('20000'),
                                      group_discount_enabled=True, group_discount_pct=D('10'))
        assert c.group_discount_amount == D('2000.00')
        assert c.net_tuition_fee == D('18000.00')
        assert c.vat_amount_non_saudi == D('2700.00')
        assert c.final_net_non_saudi == D('20700.00')

    def test_one_time_fees_total(self):
        c = f.TuitionFeeConfigFactory(entrance_exam_fee=D('300'), registration_fee=D('500'),
                                      reservation_fee=D('2000'))
        assert c.total_one_time_fees == D('2800.00')

    def _inst(self, config, kind, amount):
        return TuitionInstallment.objects.create(config=config, installment_type=kind, amount=D(amount))

    def test_valid_installments(self):
        c = f.TuitionFeeConfigFactory(gross_tuition_fee=D('20000'), num_payments=2,
                                      reservation_fee=D('2000'))
        self._inst(c, TuitionInstallment.RESERVATION, '2000')
        self._inst(c, TuitionInstallment.FIRST, '10000')
        self._inst(c, TuitionInstallment.SECOND, '10000')
        assert c.validate_installments() == []
        assert c.installments_total == D('20000.00')   # reservation excluded

    def test_no_installments_is_valid(self):
        assert f.TuitionFeeConfigFactory().validate_installments() == []

    def test_installments_not_matching_net_tuition(self):
        c = f.TuitionFeeConfigFactory(gross_tuition_fee=D('20000'), num_payments=2)
        self._inst(c, TuitionInstallment.FIRST, '10000')
        self._inst(c, TuitionInstallment.SECOND, '9000')
        errors = c.validate_installments()
        assert len(errors) == 1 and 'net tuition' in errors[0]

    def test_wrong_installment_count(self):
        c = f.TuitionFeeConfigFactory(gross_tuition_fee=D('20000'), num_payments=3)
        self._inst(c, TuitionInstallment.FIRST, '10000')
        self._inst(c, TuitionInstallment.SECOND, '10000')
        assert any('Expected 3' in e for e in c.validate_installments())

    def test_reservation_mismatch(self):
        c = f.TuitionFeeConfigFactory(gross_tuition_fee=D('20000'), num_payments=2,
                                      reservation_fee=D('2000'))
        self._inst(c, TuitionInstallment.RESERVATION, '1500')
        self._inst(c, TuitionInstallment.FIRST, '10000')
        self._inst(c, TuitionInstallment.SECOND, '10000')
        assert any('Reservation' in e for e in c.validate_installments())


class TestTuitionInstallmentLabel:
    @pytest.mark.parametrize("num_payments, kind, label", [
        (2, 'RESERVATION', 'Reservation / Down Payment'),
        (2, 'FIRST',  '1st Semester'),
        (2, 'SECOND', '2nd Semester'),
        (3, 'FIRST',  '1st Semester - 1st Installment'),
        (3, 'SECOND', '1st Semester - 2nd Installment'),
        (3, 'THIRD',  '2nd Semester'),
    ])
    def test_semester_label(self, num_payments, kind, label):
        c = f.TuitionFeeConfigFactory(num_payments=num_payments)
        inst = TuitionInstallment(config=c, installment_type=kind, amount=D('1'))
        assert inst.semester_label == label


# ── PaymentPlanInstallment ───────────────────────────────────────────────────

class TestPaymentPlanInstallment:
    @pytest.mark.parametrize("paid, due_offset, expected", [
        ('0',    5,  PaymentPlanInstallment.UNPAID),
        ('0',   -5,  PaymentPlanInstallment.OVERDUE),
        ('100',  5,  PaymentPlanInstallment.PARTIAL),
        ('100', -5,  PaymentPlanInstallment.PARTIAL),   # partially paid is never "overdue"
        ('500',  5,  PaymentPlanInstallment.PAID),
    ])
    def test_refresh_status(self, paid, due_offset, expected):
        inst = f.PaymentPlanInstallmentFactory(
            amount=D('500'), paid_amount=D(paid),
            due_date=TODAY + datetime.timedelta(days=due_offset))
        inst.refresh_status()
        assert inst.status == expected

    def test_balance(self):
        inst = f.PaymentPlanInstallmentFactory(amount=D('500'), paid_amount=D('120.50'))
        assert inst.balance == D('379.50')


# ── ExternalCandidatePayment ─────────────────────────────────────────────────

class TestExternalCandidatePayment:
    def test_vat_and_total_computed_on_save(self):
        p = f.ExternalCandidatePaymentFactory(amount=D('500'), vat_rate=D('15'))
        assert p.vat_amount == D('75.00')
        assert p.total == D('575.00')

    def test_zero_vat(self):
        p = f.ExternalCandidatePaymentFactory(amount=D('500'), vat_rate=D('0'))
        assert p.total == D('500.00')

    def test_identifiers(self):
        p = f.ExternalCandidatePaymentFactory()
        assert p.receipt_number.startswith('EXT-')
        assert p.candidate.candidate_id.startswith('EXT-')
