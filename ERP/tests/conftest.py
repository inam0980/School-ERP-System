"""
Shared pytest fixtures and hooks for the whole ERP test-suite.

Layout
------
tests/unit/         → isolated tests of one model / form / helper (marked `unit`)
tests/integration/  → full request/response tests through the Django client (marked `integration`)

Run only one layer:   pytest -m unit      |   pytest -m integration
"""
import pytest

from accounts.models import CustomUser
from tests import factories as f


# ── Auto-mark tests by folder so `-m unit` / `-m integration` just work ──────

def pytest_collection_modifyitems(config, items):
    for item in items:
        path = str(item.fspath).replace('\\', '/')
        if '/tests/unit/' in path:
            item.add_marker(pytest.mark.unit)
        elif '/tests/integration/' in path:
            item.add_marker(pytest.mark.integration)


# ── Users, one per role ──────────────────────────────────────────────────────

@pytest.fixture
def super_admin(db):
    return f.SuperAdminFactory()


@pytest.fixture
def admin(db):
    return f.UserFactory(role=CustomUser.ADMIN)


@pytest.fixture
def teacher(db):
    return f.TeacherFactory()


@pytest.fixture
def accountant(db):
    return f.AccountantFactory()


@pytest.fixture
def staff_user(db):
    return f.StaffUserFactory()


@pytest.fixture
def parent(db):
    return f.ParentFactory()


ALL_ROLES = [r for r, _ in CustomUser.ROLE_CHOICES]


@pytest.fixture
def login(client):
    """`login(user)` → logged-in client. Keeps tests one line shorter."""
    def _login(user):
        client.force_login(user)
        return client
    return _login


# ── A small but complete school, for integration tests ──────────────────────

@pytest.fixture
def school(db):
    """
    One division → grade → section, with a current academic year, a subject,
    a study mode, an active Saudi student and an active expat student.
    Returned as a simple namespace so tests read `school.student`.
    """
    from types import SimpleNamespace

    year     = f.AcademicYearFactory(is_current=True)
    division = f.DivisionFactory()
    grade    = f.GradeFactory(division=division, order=1)
    section  = f.SectionFactory(grade=grade)
    subject  = f.SubjectFactory(grade=grade, division=division)
    mode     = f.StudyModeFactory()

    common = dict(division=division, grade=grade, section=section, academic_year=year)
    return SimpleNamespace(
        year=year, division=division, grade=grade, section=section,
        subject=subject, study_mode=mode,
        student=f.StudentFactory(**common),
        expat=f.ExpatStudentFactory(**common),
    )
