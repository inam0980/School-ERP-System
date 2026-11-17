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

    # ── Decided 2026-11-17 (ZATCA): each paid fee is invoiced exactly once ──

    def _gen(self, client, student):
        return client.post(reverse('fees:generate_invoice', args=[student.pk]))

    def test_second_click_does_not_reinvoice_and_opens_existing(self, login, accountant, school, fee):
        f.PaymentFactory(student_fee=fee, paid_amount=D('1000'))
        client = login(accountant)
        self._gen(client, school.student)
        resp = self._gen(client, school.student)
        inv = TaxInvoice.objects.get()
        assert resp['Location'] == reverse('fees:invoice_print', args=[inv.pk])
        assert inv.first_printed_at is None            # the original is not pre-marked as a copy

    def test_new_invoice_contains_only_newly_paid_fees(self, login, accountant, school, fee):
        f.PaymentFactory(student_fee=fee, paid_amount=D('1000'))
        client = login(accountant)
        self._gen(client, school.student)
        bus = f.StudentFeeFactory(student=school.student, amount=D('300'),
                                  fee_structure=f.FeeStructureItemFactory(fee_type=f.FeeTypeFactory(name='Bus')))
        f.PaymentFactory(student_fee=bus, paid_amount=D('300'))
        self._gen(client, school.student)
        first, second = TaxInvoice.objects.order_by('pk')
        assert [li['student_fee_id'] for li in first.line_items_json] == [fee.pk]
        assert [li['student_fee_id'] for li in second.line_items_json] == [bus.pk]
        assert second.total == D('300')

    def test_fees_on_legacy_invoices_are_not_reinvoiced(self, login, accountant, school, fee):
        """Invoices made before this fix have no student_fee_id — match them by line content."""
        f.PaymentFactory(student_fee=fee, paid_amount=D('1000'))
        TaxInvoice.objects.create(
            student=school.student, subtotal=D('1000'), total=D('1000'), status=TaxInvoice.ISSUED,
            line_items_json=[{'description': 'Books', 'qty': 1, 'gross_amount': 1000.0, 'discount': 0.0,
                              'net_before_vat': 1000.0, 'vat_rate': 0, 'vat': 0.0, 'total': 1000.0}])
        self._gen(login(accountant), school.student)
        assert TaxInvoice.objects.count() == 1

    def test_credit_notes_are_not_counted_as_invoices(self, login, accountant, school, fee):
        f.PaymentFactory(student_fee=fee, paid_amount=D('1000'))
        TaxInvoice.objects.create(
            student=school.student, status=TaxInvoice.ISSUED, invoice_type=TaxInvoice.INVOICE_TYPE_CREDIT_NOTE,
            line_items_json=[{'description': 'Books', 'gross_amount': 1000.0, 'discount': 0.0, 'student_fee_id': fee.pk}])
        self._gen(login(accountant), school.student)
        assert TaxInvoice.objects.filter(invoice_type=TaxInvoice.INVOICE_TYPE_STANDARD).count() == 1

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


# ── Payment plans (installments) ─────────────────────────────────────────────

class TestPaymentPlan:
    @pytest.fixture
    def tuition(self, school):
        item = f.FeeStructureItemFactory(fee_type=f.FeeTypeFactory(name='1st Semester'), amount=D('10000'))
        return f.StudentFeeFactory(student=school.student, fee_structure=item, amount=D('10000'))

    def _post(self, client, sf, rows, **extra):
        today = datetime.date.today()
        data = {'installment_count': len(rows)}
        for i, (amount, sem) in enumerate(rows, start=1):
            data.update({f'inst_amount_{i}': amount, f'inst_semester_{i}': sem,
                         f'inst_due_{i}': (today + datetime.timedelta(days=30 * i)).isoformat()})
        data.update(extra)
        return client.post(reverse('fees:payment_plan_setup', args=[sf.pk]), data)

    def test_create_plan(self, login, accountant, tuition):
        from fees.models import PaymentPlan
        resp = self._post(login(accountant), tuition,
                          [('2500', 1), ('2500', 1), ('5000', 2)])
        assert resp.status_code == 302
        plan = PaymentPlan.objects.get(student_fee=tuition)
        assert [(i.installment_no, i.semester, i.amount) for i in plan.installments.all()] == \
               [(1, 1, D('2500')), (2, 1, D('2500')), (3, 2, D('5000'))]

    @pytest.mark.regression
    @pytest.mark.parametrize("rows", [
        [('5000', 1), ('4999.50', 2)],          # 0.50 short → fee could never reach PAID
        [('5000.50', 1), ('5000', 2)],          # 0.50 over
    ])
    def test_bug21_total_must_equal_balance_exactly(self, login, accountant, tuition, rows):
        from fees.models import PaymentPlan
        resp = self._post(login(accountant), tuition, rows)
        assert resp.status_code == 200
        assert not PaymentPlan.objects.exists()

    def test_odd_halala_split_between_semesters(self, login, accountant, school):
        from fees.models import PaymentPlan
        item = f.FeeStructureItemFactory(fee_type=f.FeeTypeFactory(name='2nd Semester'), amount=D('1000.01'))
        sf = f.StudentFeeFactory(student=school.student, fee_structure=item, amount=D('1000.01'))
        self._post(login(accountant), sf, [('500.00', 1), ('500.01', 2)])
        assert PaymentPlan.objects.filter(student_fee=sf).exists()

    def test_paying_every_installment_marks_fee_paid(self, login, accountant, school, tuition):
        from fees.models import PaymentPlan
        client = login(accountant)
        self._post(client, tuition, [('5000', 1), ('5000', 2)])
        insts = PaymentPlan.objects.get(student_fee=tuition).installments.all()
        client.post(f"{reverse('fees:collection')}?student_id={school.student.pk}", {
            'student_id': school.student.pk, 'selected_installments': [i.pk for i in insts],
            **{f'inst_amount_{i.pk}': str(i.amount) for i in insts}, 'payment_method': 'BANK'})
        tuition.refresh_from_db()
        assert tuition.status == StudentFee.PAID and tuition.balance == D('0')

    def test_semester_cannot_go_backwards(self, login, accountant, tuition):
        from fees.models import PaymentPlan
        self._post(login(accountant), tuition, [('2500', 1), ('5000', 2), ('2500', 1)])
        assert not PaymentPlan.objects.exists()

    def test_both_semesters_required(self, login, accountant, tuition):
        from fees.models import PaymentPlan
        self._post(login(accountant), tuition, [('5000', 1), ('5000', 1)])
        assert not PaymentPlan.objects.exists()

    @pytest.mark.parametrize("bad", ['NaN', 'Infinity', '-100', 'abc'])
    def test_bad_amounts_rejected_without_crash(self, login, accountant, tuition, bad):
        from fees.models import PaymentPlan
        assert self._post(login(accountant), tuition, [(bad, 1), ('5000', 2)]).status_code == 200
        assert not PaymentPlan.objects.exists()

    def test_replacing_plan(self, login, accountant, tuition):
        from fees.models import PaymentPlan
        client = login(accountant)
        self._post(client, tuition, [('5000', 1), ('5000', 2)])
        self._post(client, tuition, [('2500', 1), ('2500', 1), ('2500', 2), ('2500', 2)])
        assert PaymentPlan.objects.get(student_fee=tuition).installments.count() == 4

    def test_fully_paid_fee_needs_no_plan(self, login, accountant, tuition):
        f.PaymentFactory(student_fee=tuition, paid_amount=D('10000'))
        resp = login(accountant).get(reverse('fees:payment_plan_setup', args=[tuition.pk]))
        assert resp.status_code == 302

    def test_delete_requires_post(self, login, accountant, tuition):
        from fees.models import PaymentPlan
        plan = f.PaymentPlanFactory(student_fee=tuition)
        client = login(accountant)
        client.get(reverse('fees:payment_plan_delete', args=[plan.pk]))
        assert PaymentPlan.objects.filter(pk=plan.pk).exists()
        client.post(reverse('fees:payment_plan_delete', args=[plan.pk]))
        assert not PaymentPlan.objects.filter(pk=plan.pk).exists()


# ── Assigning fees to one student ────────────────────────────────────────────

class TestAssignStudentFee:
    @pytest.fixture
    def structure(self, school):
        s = f.FeeStructureFactory(academic_year=school.year, grade=school.grade)
        books = f.FeeStructureItemFactory(structure=s, fee_type=f.FeeTypeFactory(name='Books'), amount=D('800'))
        bus = f.FeeStructureItemFactory(structure=s, fee_type=f.TaxableFeeTypeFactory(), amount=D('2000'))
        return s, books, bus

    def _post(self, client, student, structure, items, pct='', **extra):
        return client.post(reverse('fees:assign_student_fee', args=[student.pk]), {
            'structure_id': structure.pk, 'item_ids': [i.pk for i in items],
            'discount_pct': pct, 'due_date': '2030-01-31', **extra})

    def test_assigns_items_with_vat_for_expat(self, login, accountant, school, structure):
        s, books, bus = structure
        self._post(login(accountant), school.expat, s, [books, bus])
        fees = {sf.fee_structure.fee_type.name: sf for sf in StudentFee.objects.filter(student=school.expat)}
        assert fees['Books'].net_amount == D('800.00')
        assert fees['Transport'].net_amount == D('2300.00')          # 15 % VAT for Iqama holder
        assert fees['Books'].due_date == datetime.date(2030, 1, 31)

    def test_discount_applied(self, login, accountant, school, structure):
        s, books, _ = structure
        self._post(login(accountant), school.student, s, [books], pct='25')
        sf = StudentFee.objects.get(student=school.student)
        assert (sf.discount, sf.net_amount) == (D('200.00'), D('600.00'))

    def test_assigning_twice_does_not_duplicate(self, login, accountant, school, structure):
        s, books, _ = structure
        client = login(accountant)
        self._post(client, school.student, s, [books])
        self._post(client, school.student, s, [books])
        assert StudentFee.objects.filter(student=school.student).count() == 1

    def test_structure_of_another_grade_rejected(self, login, accountant, school):
        other = f.FeeStructureFactory(academic_year=school.year, grade=f.GradeFactory(division=school.division))
        item = f.FeeStructureItemFactory(structure=other)
        resp = self._post(login(accountant), school.student, other, [item])
        assert resp.status_code == 404 and not StudentFee.objects.exists()

    @pytest.mark.regression
    @pytest.mark.parametrize("pct", ['abc', 'NaN', 'Infinity', '-20', '120'])
    def test_bug24_bad_discount_rejected_without_crash(self, login, accountant, school, structure, pct):
        s, books, _ = structure
        resp = self._post(login(accountant), school.student, s, [books], pct=pct)
        assert resp.status_code == 302
        assert not StudentFee.objects.filter(student=school.student).exists()

    @pytest.mark.regression
    @pytest.mark.parametrize("amount", ['Infinity', 'NaN', '-5', 'abc'])
    def test_bug24_bad_additional_fee_amount_skipped_without_crash(self, login, accountant, school, amount):
        resp = login(accountant).post(reverse('fees:assign_student_fee', args=[school.student.pk]), {
            'adhoc_fee_type[]': [f.FeeTypeFactory(name='Trip').pk], 'adhoc_amount[]': [amount],
            'adhoc_note[]': [''], 'discount_pct': ''})
        assert resp.status_code == 302
        assert not StudentFee.objects.filter(student=school.student).exists()

    def test_additional_fee(self, login, accountant, school):
        login(accountant).post(reverse('fees:assign_student_fee', args=[school.student.pk]), {
            'adhoc_fee_type[]': [f.FeeTypeFactory(name='Trip').pk], 'adhoc_amount[]': ['350'],
            'adhoc_note[]': ['Museum visit'], 'discount_pct': ''})
        sf = StudentFee.objects.get(student=school.student)
        assert sf.net_amount == D('350.00')


# ── Fee reminder emails ──────────────────────────────────────────────────────

class TestFeeReminders:
    @pytest.fixture
    def overdue(self, school):
        past = datetime.date.today() - datetime.timedelta(days=10)
        school.student.father_email = 'father@example.com'
        school.student.save()
        return f.StudentFeeFactory(student=school.student, amount=D('1200'), due_date=past)

    def test_emails_parent_of_defaulter(self, login, accountant, overdue, mailoutbox):
        resp = login(accountant).post(reverse('fees:send_reminders'))
        assert resp.status_code == 302
        assert len(mailoutbox) == 1
        mail = mailoutbox[0]
        assert mail.to == ['father@example.com']
        assert 'SAR 1200.00' in mail.subject and overdue.student.full_name in mail.body

    def test_fees_contact_email_takes_priority(self, login, accountant, overdue, mailoutbox):
        overdue.student.fees_contact_email = 'accounts@family.sa'
        overdue.student.save()
        login(accountant).post(reverse('fees:send_reminders'))
        assert mailoutbox[0].to == ['accounts@family.sa']

    def test_one_email_per_student_with_all_lines(self, login, accountant, overdue, mailoutbox):
        f.StudentFeeFactory(student=overdue.student, amount=D('300'), due_date=overdue.due_date,
                            fee_structure=f.FeeStructureItemFactory(fee_type=f.FeeTypeFactory(name='Bus')))
        login(accountant).post(reverse('fees:send_reminders'))
        assert len(mailoutbox) == 1 and 'SAR 1500.00' in mailoutbox[0].subject

    def test_paid_and_not_yet_due_fees_are_not_chased(self, login, accountant, school, mailoutbox):
        school.student.father_email = 'father@example.com'; school.student.save()
        paid = f.StudentFeeFactory(student=school.student, amount=D('100'),
                                   due_date=datetime.date.today() - datetime.timedelta(days=5))
        f.PaymentFactory(student_fee=paid, paid_amount=D('100'))
        f.StudentFeeFactory(student=school.student, amount=D('100'),
                            due_date=datetime.date.today() + datetime.timedelta(days=5),
                            fee_structure=f.FeeStructureItemFactory(fee_type=f.FeeTypeFactory(name='Bus')))
        login(accountant).post(reverse('fees:send_reminders'))
        assert mailoutbox == []

    def test_no_email_on_file_is_skipped(self, login, accountant, overdue, mailoutbox):
        overdue.student.father_email = ''; overdue.student.save()
        login(accountant).post(reverse('fees:send_reminders'))
        assert mailoutbox == []

    def test_mail_server_failure_is_reported_not_crash(self, login, accountant, overdue, monkeypatch):
        def boom(*a, **k):
            raise ConnectionRefusedError('smtp down')
        monkeypatch.setattr('django.core.mail.send_mail', boom)
        resp = login(accountant).post(reverse('fees:send_reminders'), follow=True)
        assert resp.status_code == 200 and '1 failed' in resp.content.decode()

    def test_get_not_allowed_and_teachers_denied(self, login, accountant, teacher, overdue, mailoutbox):
        assert login(accountant).get(reverse('fees:send_reminders')).status_code == 405
        login(teacher).post(reverse('fees:send_reminders'))
        assert mailoutbox == []
