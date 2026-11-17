"""
recalc_student_fees — re-prices StudentFee.net_amount after a student's ID type
(Saudi / Iqama) is corrected.

Decided 2026-11-17: by default it must NOT touch fees that already have payments
(re-billing a settled fee is a finance decision), and whatever it changes must
get its status refreshed (it used to leave a now-underpaid fee marked PAID).
"""
from decimal import Decimal as D
from io import StringIO

import pytest
from django.core.management import call_command

from fees.models import StudentFee
from students.models import Student
from tests import factories as f

pytestmark = pytest.mark.django_db


def _mispriced_fee(paid=None):
    """A taxable fee priced as Saudi (0 % VAT) for a student who is really an Iqama holder."""
    s = f.StudentFactory()
    item = f.FeeStructureItemFactory(fee_type=f.TaxableFeeTypeFactory(), amount=D('1000'))
    fee = f.StudentFeeFactory(student=s, fee_structure=item, amount=D('1000'))
    assert fee.net_amount == D('1000.00')
    if paid:
        f.PaymentFactory(student_fee=fee, paid_amount=D(paid))
    Student.objects.filter(pk=s.pk).update(id_type=Student.IQAMA)    # ID type corrected later
    return StudentFee.objects.get(pk=fee.pk)


def _run(*args):
    out = StringIO()
    call_command('recalc_student_fees', *args, stdout=out)
    return out.getvalue()


def test_unpaid_fee_is_repriced():
    fee = _mispriced_fee()
    _run()
    fee.refresh_from_db()
    assert fee.net_amount == D('1150.00')


def test_dry_run_changes_nothing():
    fee = _mispriced_fee()
    _run('--dry-run')
    fee.refresh_from_db()
    assert fee.net_amount == D('1000.00')


@pytest.mark.parametrize("paid", ['1000', '400'])
def test_fees_with_payments_are_skipped_by_default(paid):
    fee = _mispriced_fee(paid=paid)
    before = (fee.net_amount, fee.status)
    out = _run()
    fee.refresh_from_db()
    assert (fee.net_amount, fee.status) == before
    assert 'skipped' in out.lower() and '--include-paid' in out


def test_include_paid_reprices_and_refreshes_status():
    """A fully paid 1000 fee re-priced to 1150 must become PARTIAL, not stay PAID."""
    fee = _mispriced_fee(paid='1000')
    assert fee.status == StudentFee.PAID
    _run('--include-paid')
    fee.refresh_from_db()
    assert fee.net_amount == D('1150.00')
    assert fee.status == StudentFee.PARTIAL and fee.balance == D('150.00')


def test_correct_fees_untouched():
    item = f.FeeStructureItemFactory(fee_type=f.TaxableFeeTypeFactory(), amount=D('1000'))
    fee = f.StudentFeeFactory(student=f.ExpatStudentFactory(), fee_structure=item, amount=D('1000'))
    out = _run()
    assert '0 record' in out.lower() or 'fixed 0' in out.lower()
    fee.refresh_from_db()
    assert fee.net_amount == D('1150.00')
