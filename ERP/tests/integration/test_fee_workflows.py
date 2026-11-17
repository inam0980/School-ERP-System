"""
End-to-end fee workflows driven through the real views:
collect → receipt → void / refund → invoice, plus payroll and bank verification.
"""
import datetime
from decimal import Decimal as D

import pytest
from django.urls import reverse

from fees.models import Payment, Refund, StudentFee, TaxInvoice
from tests import factories as f

pytestmark = pytest.mark.django_db


@pytest.fixture
def fee(school):
    item = f.FeeStructureItemFactory(fee_type=f.FeeTypeFactory(name='Books'), amount=D('1000'))
    return f.StudentFeeFactory(student=school.student, fee_structure=item, amount=D('1000'))


def _collect(client, student, fee, amount, **extra):
    data = {
        'student_id': student.pk, 'selected_fees': [fee.pk],
        f'amount_{fee.pk}': str(amount), f'discount_pct_{fee.pk}': '',
        'payment_method': Payment.CREDIT_CARD, 'payment_date': datetime.date.today().isoformat(),
        **extra,
    }
    return client.post(f"{reverse('fees:collection')}?student_id={student.pk}", data)


# ── Collection ───────────────────────────────────────────────────────────────

class TestFeeCollection:
    def test_page_lists_outstanding_fee(self, login, accountant, school, fee):
        resp = login(accountant).get(reverse('fees:collection'), {'student_id': school.student.pk})
        assert resp.status_code == 200
        assert fee in resp.context['dues']

    def test_partial_payment(self, login, accountant, school, fee):
        resp = _collect(login(accountant), school.student, fee, '400')
        assert resp.status_code == 302 and 'receipts=' in resp['Location']
        fee.refresh_from_db()
        assert fee.status == StudentFee.PARTIAL and fee.balance == D('600')
        p = Payment.objects.get(student_fee=fee)
        assert p.collected_by == accountant and p.paid_amount == D('400')

    def test_full_payment_marks_paid_and_hides_from_dues(self, login, accountant, school, fee):
        client = login(accountant)
        _collect(client, school.student, fee, '1000')
        fee.refresh_from_db()
        assert fee.status == StudentFee.PAID
        resp = client.get(reverse('fees:collection'), {'student_id': school.student.pk})
        assert fee not in resp.context['dues']

    @pytest.mark.parametrize("amount", ['1000.01', '0', '-5', 'abc'])
    def test_invalid_amounts_are_rejected(self, login, accountant, school, fee, amount):
        _collect(login(accountant), school.student, fee, amount)
        assert not Payment.objects.exists()
        fee.refresh_from_db()
        assert fee.status == StudentFee.UNPAID

    def test_discount_percentage_reduces_amount_due(self, login, accountant, school, fee):
        _collect(login(accountant), school.student, fee, '900', **{f'discount_pct_{fee.pk}': '10'})
        fee.refresh_from_db()
        assert fee.discount == D('100.00')
        assert fee.net_amount == D('900.00')
        assert fee.status == StudentFee.PAID

    def test_cannot_pay_another_students_fee(self, login, accountant, school, fee):
        """Fee pk in the POST must belong to the selected student."""
        _collect(login(accountant), school.expat, fee, '100')
        assert not Payment.objects.exists()

    def test_nothing_selected_shows_error(self, login, accountant, school, fee):
        resp = login(accountant).post(
            f"{reverse('fees:collection')}?student_id={school.student.pk}",
            {'student_id': school.student.pk})
        assert resp.status_code == 200
        assert not Payment.objects.exists()

    def test_installment_payment_updates_plan_and_fee(self, login, accountant, school, fee):
        plan = f.PaymentPlanFactory(student_fee=fee)
        inst = f.PaymentPlanInstallmentFactory(plan=plan, installment_no=1, amount=D('500'))
        login(accountant).post(
            f"{reverse('fees:collection')}?student_id={school.student.pk}",
            {'student_id': school.student.pk, 'selected_installments': [inst.pk],
             f'inst_amount_{inst.pk}': '500', 'payment_method': Payment.BANK})
        inst.refresh_from_db(); fee.refresh_from_db()
        assert inst.status == 'PAID' and inst.paid_amount == D('500')
        assert fee.status == StudentFee.PARTIAL
        assert Payment.objects.get().installment == inst

    def test_receipt_page_shows_receipt_number(self, login, accountant, school, fee):
        client = login(accountant)
        _collect(client, school.student, fee, '250')
        p = Payment.objects.get()
        resp = client.get(reverse('fees:receipt_print', args=[p.pk]))
        assert resp.status_code == 200 and p.receipt_number.encode() in resp.content


# ── Void ─────────────────────────────────────────────────────────────────────

class TestVoidPayment:
    def test_admin_voids_payment_and_balance_is_restored(self, login, admin, fee):
        p = f.PaymentFactory(student_fee=fee, paid_amount=D('1000'))
        assert StudentFee.objects.get(pk=fee.pk).status == StudentFee.PAID
        login(admin).post(reverse('fees:void_payment', args=[p.pk]), {'reason': 'Wrong student'})
        p.refresh_from_db(); fee.refresh_from_db()
        assert p.is_voided and p.voided_by == admin and p.void_reason == 'Wrong student'
        assert fee.status == StudentFee.UNPAID and fee.balance == D('1000')

    def test_reason_is_required(self, login, admin, fee):
        p = f.PaymentFactory(student_fee=fee)
        login(admin).post(reverse('fees:void_payment', args=[p.pk]), {'reason': '  '})
        p.refresh_from_db()
        assert not p.is_voided

    def test_accountant_cannot_void(self, login, accountant, fee):
        p = f.PaymentFactory(student_fee=fee)
        login(accountant).post(reverse('fees:void_payment', args=[p.pk]), {'reason': 'x'})
        p.refresh_from_db()
        assert not p.is_voided

    def test_payment_with_refund_cannot_be_voided(self, login, admin, fee):
        p = f.PaymentFactory(student_fee=fee, paid_amount=D('500'))
        f.RefundFactory(payment=p, amount=D('100'))
        login(admin).post(reverse('fees:void_payment', args=[p.pk]), {'reason': 'x'})
        p.refresh_from_db()
        assert not p.is_voided

    def test_void_rolls_back_installment(self, login, admin, fee):
        plan = f.PaymentPlanFactory(student_fee=fee)
        inst = f.PaymentPlanInstallmentFactory(plan=plan, amount=D('500'), paid_amount=D('500'))
        p = f.PaymentFactory(student_fee=fee, installment=inst, paid_amount=D('500'))
        login(admin).post(reverse('fees:void_payment', args=[p.pk]), {'reason': 'x'})
        inst.refresh_from_db()
        assert inst.paid_amount == D('0.00') and inst.status in ('UNPAID', 'OVERDUE')

    def test_get_is_not_allowed(self, login, admin, fee):
        p = f.PaymentFactory(student_fee=fee)
        assert login(admin).get(reverse('fees:void_payment', args=[p.pk])).status_code == 405


# ── Refund ───────────────────────────────────────────────────────────────────

class TestRefundPayment:
    def test_partial_refund(self, login, admin, fee):
        p = f.PaymentFactory(student_fee=fee, paid_amount=D('1000'))
        login(admin).post(reverse('fees:refund_payment', args=[p.pk]),
                          {'amount': '300', 'reason': 'Deposit returned', 'method': Payment.BANK})
        r = Refund.objects.get()
        assert r.amount == D('300') and r.refunded_by == admin
        fee.refresh_from_db()
        assert fee.status == StudentFee.PARTIAL and fee.balance == D('300')

    @pytest.mark.parametrize("amount", ['1000.01', '0', 'abc'])
    def test_cannot_refund_more_than_paid_or_invalid(self, login, admin, fee, amount):
        p = f.PaymentFactory(student_fee=fee, paid_amount=D('1000'))
        login(admin).post(reverse('fees:refund_payment', args=[p.pk]), {'amount': amount, 'reason': 'x'})
        assert not Refund.objects.exists()

    def test_cumulative_refunds_capped_at_paid_amount(self, login, admin, fee):
        p = f.PaymentFactory(student_fee=fee, paid_amount=D('1000'))
        client = login(admin)
        client.post(reverse('fees:refund_payment', args=[p.pk]), {'amount': '700', 'reason': 'a'})
        client.post(reverse('fees:refund_payment', args=[p.pk]), {'amount': '400', 'reason': 'b'})
        assert Refund.objects.count() == 1

    def test_voided_payment_cannot_be_refunded(self, login, admin, fee):
        p = f.PaymentFactory(student_fee=fee, paid_amount=D('1000'), is_voided=True)
        login(admin).post(reverse('fees:refund_payment', args=[p.pk]), {'amount': '100', 'reason': 'x'})
        assert not Refund.objects.exists()

    def test_reason_required(self, login, admin, fee):
        p = f.PaymentFactory(student_fee=fee, paid_amount=D('1000'))
        login(admin).post(reverse('fees:refund_payment', args=[p.pk]), {'amount': '100', 'reason': ''})
        assert not Refund.objects.exists()


# ── Reports reflect voids ────────────────────────────────────────────────────

class TestReportsExcludeVoids:
    def test_daily_collection_excludes_voided(self, login, accountant, fee):
        f.PaymentFactory(student_fee=fee, paid_amount=D('300'))
        f.PaymentFactory(student_fee=fee, paid_amount=D('200'), is_voided=True)
        resp = login(accountant).get(reverse('fees:daily_collection'))
        assert resp.status_code == 200
        assert len(resp.context['payments']) == 1
        assert len(resp.context['voided']) == 1


# ── Tax invoice ──────────────────────────────────────────────────────────────

class TestGenerateInvoice:
    def test_no_paid_fees_redirects_to_ledger_without_invoice(self, login, accountant, school, fee):
        resp = login(accountant).post(reverse('fees:generate_invoice', args=[school.student.pk]))
        assert resp.status_code == 302 and not TaxInvoice.objects.exists()

    def test_expat_invoice_includes_vat_on_taxable_fee(self, login, accountant, school):
        item = f.FeeStructureItemFactory(fee_type=f.TaxableFeeTypeFactory(), amount=D('1000'))
        sf = f.StudentFeeFactory(student=school.expat, fee_structure=item, amount=D('1000'))
        f.PaymentFactory(student_fee=sf, paid_amount=sf.net_amount)
        login(accountant).post(reverse('fees:generate_invoice', args=[school.expat.pk]))
        inv = TaxInvoice.objects.get()
        assert (inv.subtotal, inv.tax_amount, inv.total) == (D('1000'), D('150'), D('1150'))
        assert inv.line_items_json[0]['vat_rate'] == 15

    def test_saudi_invoice_has_zero_vat(self, login, accountant, school):
        item = f.FeeStructureItemFactory(fee_type=f.TaxableFeeTypeFactory(), amount=D('1000'))
        sf = f.StudentFeeFactory(student=school.student, fee_structure=item, amount=D('1000'))
        f.PaymentFactory(student_fee=sf, paid_amount=sf.net_amount)
        login(accountant).post(reverse('fees:generate_invoice', args=[school.student.pk]))
        assert TaxInvoice.objects.get().tax_amount == D('0')

    def test_CURRENT_BEHAVIOUR_regenerating_reinvoices_same_fees(self, login, accountant, school, fee):
        """
        Pins current behaviour (pending a business decision): every call invoices
        ALL paid fees again; only `first_printed_at` marks later ones as copies.
        """
        f.PaymentFactory(student_fee=fee, paid_amount=D('1000'))
        client = login(accountant)
        client.post(reverse('fees:generate_invoice', args=[school.student.pk]))
        client.post(reverse('fees:generate_invoice', args=[school.student.pk]))
        first, second = TaxInvoice.objects.order_by('pk')
        assert first.total == second.total == D('1000')
        assert first.first_printed_at is None and second.first_printed_at is not None


# ── Payroll & bank verification ──────────────────────────────────────────────

class TestPayrollAndBank:
    def test_mark_salary_paid(self, login, admin):
        sal = f.SalaryFactory()
        login(admin).post(reverse('fees:salary_mark_paid', args=[sal.pk]), {'bank_ref': 'TRX-1'})
        sal.refresh_from_db()
        assert sal.is_paid and sal.paid_date == datetime.date.today() and sal.bank_ref == 'TRX-1'

    def test_accountant_cannot_mark_salary_paid(self, login, accountant):
        sal = f.SalaryFactory()
        login(accountant).post(reverse('fees:salary_mark_paid', args=[sal.pk]))
        sal.refresh_from_db()
        assert not sal.is_paid

    def test_bank_verify(self, login, accountant, fee):
        p = f.PaymentFactory(student_fee=fee)
        login(accountant).post(reverse('fees:bank_verify', args=[p.pk]), {'bank_ref': 'SNB-99'})
        p.refresh_from_db()
        assert p.bank_verified and p.transaction_ref == 'SNB-99'
