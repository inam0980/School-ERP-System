"""
Data-repair command for BUG-01: students created through the UI before the fix
were stored as id_type=NATIONAL_ID even when they hold an Iqama / Passport.
"""
from io import StringIO

import pytest
from django.core.management import call_command

from students.models import Student
from tests import factories as f

pytestmark = pytest.mark.django_db


def _wrongly_saudi(**ids):
    """Reproduces what the buggy form produced: an expat saved as NATIONAL_ID."""
    s = f.StudentFactory(national_id='', **ids)
    assert s.id_type == Student.NATIONAL_ID_TYPE
    return s


def _run(*args):
    out = StringIO()
    call_command('fix_student_id_types', *args, stdout=out)
    return out.getvalue()


def test_dry_run_is_the_default_and_changes_nothing():
    s = _wrongly_saudi(iqama_number='2123456789')
    out = _run()
    s.refresh_from_db()
    assert s.id_type == Student.NATIONAL_ID_TYPE
    assert 'DRY RUN' in out and s.student_id in out


def test_apply_fixes_iqama_and_passport_holders():
    iq = _wrongly_saudi(iqama_number='2123456789')
    pp = _wrongly_saudi(passport_number='P1234567')
    _run('--apply')
    iq.refresh_from_db(); pp.refresh_from_db()
    assert iq.id_type == Student.IQAMA
    assert pp.id_type == Student.PASSPORT_ID


def test_genuine_saudis_are_untouched():
    saudi = f.StudentFactory(national_id='1123456789', iqama_number='')
    both = f.StudentFactory(national_id='1123456780', iqama_number='2123456789')
    _run('--apply')
    for s in (saudi, both):
        s.refresh_from_db()
        assert s.id_type == Student.NATIONAL_ID_TYPE


def test_does_not_reprice_existing_fees():
    """Re-billing existing fees is a finance decision — the command must not do it."""
    s = _wrongly_saudi(iqama_number='2123456789')
    item = f.FeeStructureItemFactory(fee_type=f.TaxableFeeTypeFactory())
    fee = f.StudentFeeFactory(student=s, fee_structure=item)
    before = fee.net_amount
    out = _run('--apply')
    fee.refresh_from_db()
    assert fee.net_amount == before
    assert '1 existing fee' in out          # but it tells the operator what's affected
