"""
Unit tests for model logic outside the fees app:
accounts, core, students, academics, attendance, staff.
"""
import datetime
import re
from decimal import Decimal as D

import pytest

from accounts.models import CustomUser
from academics.models import Mark
from attendance.models import Attendance
from core.models import AcademicYear
from staff.models import VacationRequest
from students.models import Student, StudentDocument
from tests import factories as f

pytestmark = pytest.mark.django_db

TODAY = datetime.date.today()


# ── accounts ─────────────────────────────────────────────────────────────────

class TestCustomUserManager:
    def test_create_user_requires_email(self):
        with pytest.raises(ValueError):
            CustomUser.objects.create_user('u1', '', 'pw')

    def test_create_user_hashes_password(self):
        u = CustomUser.objects.create_user('u1', 'U1@School.SA', 'secret', full_name='U')
        assert u.check_password('secret')
        assert u.password != 'secret'
        assert u.email == 'U1@school.sa'          # domain normalised

    def test_create_superuser_defaults(self):
        u = CustomUser.objects.create_superuser('root', 'root@school.sa', 'pw', full_name='R')
        assert u.is_superuser and u.is_staff
        assert u.role == CustomUser.SUPER_ADMIN


class TestRoleProperties:
    @pytest.mark.parametrize("role, admin, teacher, accountant", [
        ('SUPER_ADMIN', True,  False, False),
        ('ADMIN',       True,  False, False),
        ('TEACHER',     False, True,  False),
        ('ACCOUNTANT',  False, False, True),
        ('STAFF',       False, False, False),
        ('PARENT',      False, False, False),
    ])
    def test_role_flags(self, role, admin, teacher, accountant):
        u = CustomUser(role=role)
        assert u.is_admin_role is admin
        assert u.is_teacher is teacher
        assert u.is_accountant is accountant
        assert u.is_super_admin is (role == 'SUPER_ADMIN')


# ── core ─────────────────────────────────────────────────────────────────────

class TestAcademicYear:
    def test_only_one_current_year(self):
        a = f.AcademicYearFactory(name='2024-25', is_current=True)
        b = f.AcademicYearFactory(name='2025-26', start_date=datetime.date(2025, 9, 1),
                                  end_date=datetime.date(2026, 6, 30), is_current=True)
        a.refresh_from_db()
        assert b.is_current and not a.is_current
        assert AcademicYear.objects.filter(is_current=True).count() == 1

    def test_saving_non_current_year_leaves_current_alone(self):
        a = f.AcademicYearFactory(name='2024-25', is_current=True)
        f.AcademicYearFactory(name='2023-24', is_current=False)
        a.refresh_from_db()
        assert a.is_current


# ── students ─────────────────────────────────────────────────────────────────

class TestStudentModel:
    def test_student_id_generated_with_year_and_division(self):
        s = f.StudentFactory(academic_year=f.AcademicYearFactory(name='2024-25'))
        assert re.fullmatch(r'AKS-2024-[A-Z]{2}-\d{6}', s.student_id), s.student_id

    def test_student_id_is_stable_across_saves(self):
        s = f.StudentFactory()
        original = s.student_id
        s.full_name = 'Renamed'
        s.save()
        assert s.student_id == original

    def test_student_ids_are_unique(self):
        ids = {f.StudentFactory().student_id for _ in range(15)}
        assert len(ids) == 15

    @pytest.mark.parametrize("id_type, saudi", [
        (Student.NATIONAL_ID_TYPE, True),
        (Student.IQAMA, False),
        (Student.PASSPORT_ID, False),
    ])
    def test_is_saudi_follows_id_type(self, id_type, saudi):
        assert Student(id_type=id_type).is_saudi is saudi

    def test_age_before_and_after_birthday(self):
        ten_years_ago = TODAY.replace(year=TODAY.year - 10)
        assert Student(dob=ten_years_ago).age == 10
        assert Student(dob=ten_years_ago + datetime.timedelta(days=1)).age == 9

    def test_reminder_contact_priority(self):
        s = Student(guardian_phone='3', mother_mobile='2', father_mobile='1')
        assert s.reminder_phone() == '1'
        s.fees_contact_phone = ' 0 '
        assert s.reminder_phone() == '0'            # explicit contact wins, trimmed
        assert Student().reminder_phone() == ''

    def test_reminder_email_falls_back_to_guardian(self):
        assert Student(guardian_email='g@x.sa').reminder_email() == 'g@x.sa'

    def test_document_filename_and_ext(self):
        doc = StudentDocument(file='students/documents/X/Passport.Scan.PDF')
        assert doc.filename == 'Passport.Scan.PDF'
        assert doc.ext == 'pdf'
        assert StudentDocument(file='a/b/noext').ext == ''


# ── academics ────────────────────────────────────────────────────────────────

class TestMarkGrading:
    def _mark(self, obtained, total=100, absent=False):
        exam = f.ExamFactory.build(total_marks=total)
        return Mark(exam=exam, obtained_marks=obtained, is_absent=absent)

    @pytest.mark.parametrize("score, letter, gpa", [
        (100, 'A+', 4.0), (90, 'A+', 4.0), (89.9, 'A', 4.0), (85, 'A', 4.0),
        (80, 'B+', 3.5), (75, 'B', 3.0), (70, 'C+', 2.5), (65, 'C', 2.0),
        (60, 'D', 1.0), (59.9, 'F', 0.0), (0, 'F', 0.0),
    ])
    def test_letter_grade_boundaries(self, score, letter, gpa):
        m = self._mark(D(str(score)))
        assert m.get_letter_grade() == letter
        assert m.get_gpa_points() == gpa

    def test_percentage_scales_by_total_marks(self):
        assert self._mark(D('40'), total=50).get_percentage() == 80.0

    def test_absent(self):
        m = self._mark(D('99'), absent=True)
        assert m.get_percentage() is None
        assert m.get_letter_grade() == 'AB'
        assert m.get_gpa_points() == 0.0
        assert m.is_passed() is False

    def test_not_entered_yet(self):
        assert self._mark(None).get_percentage() is None

    def test_pass_threshold_is_60(self):
        assert self._mark(D('60')).is_passed() is True
        assert self._mark(D('59.9')).is_passed() is False

    def test_percentage_is_rounded_before_pass_fail_decision(self):
        """
        DECIDED (2026-11-17): keep rounding to 1 dp *before* grading, so 59.95 %
        passes and 89.95 % is A+ — the percentage shown and the result always agree
        (never "60.0 %  FAIL"). Change only on a new school decision; flip these first.
        """
        assert self._mark(D('59.94')).is_passed() is False
        assert self._mark(D('59.95')).is_passed() is True
        assert self._mark(D('89.95')).get_letter_grade() == 'A+'


# ── attendance ───────────────────────────────────────────────────────────────

class TestAttendance:
    @pytest.mark.parametrize("status, present", [('P', True), ('L', True), ('A', False), ('E', False)])
    def test_is_present(self, status, present):
        assert Attendance(status=status).is_present is present

    def test_one_record_per_student_per_day(self):
        from django.db import IntegrityError, transaction
        a = f.AttendanceFactory()
        with pytest.raises(IntegrityError), transaction.atomic():
            f.AttendanceFactory(student=a.student, date=a.date)


# ── staff ────────────────────────────────────────────────────────────────────

class TestStaffModels:
    def test_vacation_duration_is_inclusive(self):
        v = VacationRequest(from_date=datetime.date(2025, 1, 1), to_date=datetime.date(2025, 1, 5))
        assert v.duration_days == 5
        v.to_date = v.from_date
        assert v.duration_days == 1

    @pytest.mark.parametrize("days, expiring", [(None, False), (30, True), (90, True), (91, False), (-1, True)])
    def test_iqama_expiring_soon_90_days(self, days, expiring):
        expiry = None if days is None else TODAY + datetime.timedelta(days=days)
        p = f.StaffProfileFactory(iqama_expiry=expiry)
        assert p.is_iqama_expiring_soon is expiring

    @pytest.mark.parametrize("days, expiring", [(None, False), (60, True), (61, False)])
    def test_moe_expiring_soon_60_days(self, days, expiring):
        expiry = None if days is None else TODAY + datetime.timedelta(days=days)
        assert f.MOEApprovalFactory(expiry_date=expiry).is_expiring_soon is expiring

    def test_staff_profile_full_name_proxies_user(self):
        p = f.StaffProfileFactory(user__full_name='Sara Ali')
        assert p.full_name == 'Sara Ali'


class TestUserDisplayNames:
    """BUG-17: templates/invoices call get_full_name(), which CustomUser lacked."""
    def test_get_full_name_returns_full_name(self):
        assert CustomUser(username='u', full_name='Fatima Al-Harbi').get_full_name() == 'Fatima Al-Harbi'

    def test_falls_back_to_username_when_name_blank(self):
        assert CustomUser(username='fh01', full_name='').get_full_name() == 'fh01'

    def test_short_name_is_first_word(self):
        assert CustomUser(username='u', full_name='Fatima Al-Harbi').get_short_name() == 'Fatima'
