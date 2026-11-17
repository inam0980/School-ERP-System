"""
Student CSV import (students:import) — creates/updates many records at once.
"""
import csv
import io

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from students.models import Student
from students.views import STUDENT_CSV_COLUMNS

pytestmark = pytest.mark.django_db


def _csv(rows):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=STUDENT_CSV_COLUMNS)
    w.writeheader()
    for r in rows:
        w.writerow(r)
    return SimpleUploadedFile('students.csv', ('﻿' + buf.getvalue()).encode('utf-8'), content_type='text/csv')


@pytest.fixture
def import_school(db):
    """Own division name: 'AMERICAN' from the factory clashes (case-insensitively)
    with the 'American' row seeded by migrations, which the importer looks up by name__iexact."""
    from types import SimpleNamespace
    from tests import factories as f
    div = f.DivisionFactory(name='Import Test Division')
    grade = f.GradeFactory(division=div, name='Import Grade')
    section = f.SectionFactory(grade=grade, name='Z')
    year = f.AcademicYearFactory(is_current=True)
    student = f.StudentFactory(division=div, grade=grade, section=section, academic_year=year)
    return SimpleNamespace(division=div, grade=grade, section=section, year=year, student=student)


@pytest.fixture
def school(import_school):
    return import_school


@pytest.fixture
def row(school):
    def _row(**over):
        base = {
            'Full Name': 'Imported Kid', 'Arabic Name': 'طفل', 'Gender': 'Male', 'Date of Birth': '2015-04-01',
            'Nationality': 'Saudi Arabia', 'ID Type': 'National ID', 'National ID': '1234567890',
            'Division': school.division.name, 'Grade': school.grade.name, 'Section': school.section.name,
            'Academic Year': school.year.name, 'Enrollment Type': 'New', 'Active': 'Yes',
        }
        base.update(over)
        return base
    return _row


def _import(client, rows):
    return client.post(reverse('students:import'), {'csv_file': _csv(rows)}, follow=True)


class TestImport:
    def test_creates_students(self, login, admin, row):
        _import(login(admin), [row(), row(**{'Full Name': 'Second Kid', 'National ID': '1234567891'})])
        assert Student.objects.filter(full_name__in=['Imported Kid', 'Second Kid']).count() == 2

    def test_updates_existing_by_student_id(self, login, admin, school, row):
        sid = school.student.student_id
        _import(login(admin), [row(**{'Student ID': sid, 'Full Name': 'Renamed By Import'})])
        school.student.refresh_from_db()
        assert school.student.full_name == 'Renamed By Import'

    def test_bad_rows_reported_good_rows_kept(self, login, admin, row):
        resp = _import(login(admin), [row(**{'Grade': 'No Such Grade'}), row(**{'Full Name': 'Good Kid'})])
        assert Student.objects.filter(full_name='Good Kid').exists()
        import html
        assert "Grade 'No Such Grade' not found" in html.unescape(resp.content.decode())

    def test_only_admins(self, login, teacher, row):
        _import(login(teacher), [row()])
        assert not Student.objects.filter(full_name='Imported Kid').exists()

    def test_non_utf8_file_reports_error_not_crash(self, login, admin):
        f = SimpleUploadedFile('s.csv', 'Full Name\nCafé\n'.encode('cp1252'), content_type='text/csv')
        resp = login(admin).post(reverse('students:import'), {'csv_file': f}, follow=True)
        assert resp.status_code == 200 and 'Import failed' in resp.content.decode()


@pytest.mark.regression
class TestBug22ImportIdTypeDerivedFromIds:
    @pytest.mark.parametrize("id_type_cell", ['', 'Residence permit', 'iqama number'])
    def test_iqama_holder_with_unclear_id_type_is_not_saudi(self, login, admin, row, id_type_cell):
        _import(login(admin), [row(**{'ID Type': id_type_cell, 'National ID': '', 'Iqama Number': '2123456789'})])
        s = Student.objects.get(full_name='Imported Kid')
        assert s.id_type == Student.IQAMA and s.is_saudi is False

    def test_passport_only(self, login, admin, row):
        _import(login(admin), [row(**{'ID Type': '', 'National ID': '', 'Passport Number': 'P998877'})])
        assert Student.objects.get(full_name='Imported Kid').id_type == Student.PASSPORT_ID

    def test_explicit_id_type_still_wins(self, login, admin, row):
        _import(login(admin), [row(**{'ID Type': 'Iqama', 'National ID': '', 'Iqama Number': '2123456789'})])
        assert Student.objects.get(full_name='Imported Kid').id_type == Student.IQAMA


@pytest.mark.regression
class TestBug23ImportGenderNeverGuessed:
    @pytest.mark.parametrize("cell, gender", [
        ('أنثى', 'F'), ('ذكر', 'M'), ('Female', 'F'), ('F', 'F'), ('Male / ذكر', 'M'), ('girl', 'F'), ('boy', 'M'),
    ])
    def test_gender_words(self, login, admin, row, cell, gender):
        _import(login(admin), [row(**{'Gender': cell})])
        assert Student.objects.get(full_name='Imported Kid').gender == gender

    @pytest.mark.parametrize("cell", ['', 'X', 'unknown'])
    def test_unknown_gender_is_a_row_error(self, login, admin, row, cell):
        resp = _import(login(admin), [row(**{'Gender': cell})])
        assert not Student.objects.filter(full_name='Imported Kid').exists()
        assert 'Gender' in resp.content.decode()
