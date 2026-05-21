"""Find rows in the CSV that don't yet exist in the DB (by name + grade + section)
and create them. Safe to run multiple times — only inserts missing students.
"""
import csv
from datetime import date as _date
from students.models import Student
from core.models import Division, Grade, Section, AcademicYear, StudyMode

CSV_PATH = r"e:\ERP_SYSTEM\students_import_3000.csv"

GENDER_MAP    = {'male': 'M', 'female': 'F'}
ID_TYPE_MAP   = {'national id': 'NATIONAL_ID', 'iqama': 'IQAMA', 'passport': 'PASSPORT'}
ENROLL_MAP    = {'new student': 'NEW', 'regular (continuing)': 'REGULAR', 'transfer': 'TRANSFER'}
FEE_CAT_MAP   = {'new': 'new', 'regular': 'regular', 'transfer': 'transfer', 'other': 'other'}
RELIGION_MAP  = {'muslim': 'Muslim', 'non-muslim': 'Non-Muslim'}

created = 0
skipped = 0
errors  = []

with open(CSV_PATH, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader, start=2):
        row = {k.strip(): (v.strip() if v else '') for k, v in row.items()}
        full_name = row.get('Full Name', '')
        if not full_name:
            continue

        div_name = row.get('Division', '')
        grd_name = row.get('Grade', '')
        sec_name = row.get('Section', '')
        yr_name  = row.get('Academic Year', '')

        try:
            division = Division.objects.get(name__iexact=div_name)
            grade    = Grade.objects.get(name__iexact=grd_name, division=division)
            section  = Section.objects.get(name__iexact=sec_name, grade=grade)
            year     = AcademicYear.objects.get(name__iexact=yr_name)
        except Exception as e:
            errors.append(f"Row {i} ({full_name}): FK lookup failed — {e}")
            continue

        # Skip if a matching student already exists
        if Student.objects.filter(
            full_name=full_name, grade=grade, section=section, academic_year=year
        ).exists():
            skipped += 1
            continue

        try:
            dob = _date.fromisoformat(row.get('Date of Birth', ''))
        except ValueError:
            dob = _date(2015, 1, 1)
        try:
            admission = _date.fromisoformat(row.get('Admission Date', '')) if row.get('Admission Date') else _date.today()
        except ValueError:
            admission = _date.today()

        sm_name    = row.get('Study Mode', '').strip()
        study_mode = StudyMode.objects.filter(name__iexact=sm_name, is_active=True).first() if sm_name else None

        try:
            s = Student(
                full_name       = full_name,
                arabic_name     = row.get('Arabic Name', ''),
                gender          = GENDER_MAP.get(row.get('Gender', '').lower(), 'M'),
                dob             = dob,
                nationality     = row.get('Nationality', 'Saudi Arabia'),
                id_type         = ID_TYPE_MAP.get(row.get('ID Type', '').lower(), 'NATIONAL_ID'),
                national_id     = row.get('National ID', ''),
                iqama_number    = row.get('Iqama Number', ''),
                passport_number = row.get('Passport Number', ''),
                religion        = RELIGION_MAP.get(row.get('Religion', '').lower(), ''),
                birth_place     = row.get('Birth Place', ''),
                division        = division,
                grade           = grade,
                section         = section,
                academic_year   = year,
                roll_number     = row.get('Roll No.', ''),
                enrollment_type = ENROLL_MAP.get(row.get('Enrollment Type', '').lower(), 'NEW'),
                study_mode      = study_mode,
                fee_category    = FEE_CAT_MAP.get(row.get('Fee Category', '').lower(), 'regular'),
                admission_date  = admission,
                is_active       = (row.get('Active', 'Yes').lower() != 'no'),
                father_name     = row.get('Father Name', ''),
                mother_name     = row.get('Mother Name', ''),
                guardian_phone  = row.get('Guardian Phone', ''),
                guardian_email  = row.get('Guardian Email', ''),
                address         = row.get('Address', ''),
            )
            s.save()                       # uses the fixed retry-on-collision logic
            created += 1
        except Exception as e:
            errors.append(f"Row {i} ({full_name}): {e}")

print(f"Created: {created}")
print(f"Skipped (already in DB): {skipped}")
print(f"Errors: {len(errors)}")
for e in errors[:10]:
    print("  ", e)
print(f"\nTotal students in DB now: {Student.objects.count()}")
