from django.db import migrations


CORRECT_GRADES = [
    ('Nursery',    0),
    ('Pre-Kinder', 1),
    ('Kinder 1',   2),
    ('Kinder 2',   3),
    ('Reception',  4),
    ('Grade 1',    5),
    ('Grade 2',    6),
    ('Grade 3',    7),
    ('Grade 4',    8),
    ('Grade 5',    9),
    ('Grade 6',    10),
    ('Grade 7',    11),
    ('Grade 8',    12),
    ('Grade 9',    13),
    ('Grade 10',   14),
    ('Grade 11',   15),
    ('Grade 12',   16),
]

OLD_GRADE_NAMES = ['KG 1', 'KG 2']


def fix_grades(apps, schema_editor):
    Division = apps.get_model('core', 'Division')
    Grade = apps.get_model('core', 'Grade')
    Section = apps.get_model('core', 'Section')

    # Remove old incorrect grades from all divisions
    Grade.objects.filter(name__in=OLD_GRADE_NAMES).delete()

    # For each existing division, ensure all correct grades + sections exist
    for division in Division.objects.all():
        for grade_name, order in CORRECT_GRADES:
            grade, _ = Grade.objects.get_or_create(
                name=grade_name,
                division=division,
                defaults={'order': order}
            )
            for section_name in ['A', 'B', 'C']:
                Section.objects.get_or_create(
                    name=section_name,
                    grade=grade,
                    defaults={'capacity': 30}
                )


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_add_default_divisions_grades_sections'),
    ]

    operations = [
        migrations.RunPython(fix_grades, migrations.RunPython.noop),
    ]
