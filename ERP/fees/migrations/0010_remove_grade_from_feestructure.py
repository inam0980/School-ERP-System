"""
Remove `grade` FK from FeeStructure so that one structure covers
an entire Division (not one per grade).  Grade selection moves to
the Bulk Assign form at assignment time.

Data changes:
  1. Clear StudentFees (they reference FeeStructureItems; items stay).
  2. Deduplicate FeeStructure rows: keep lowest-pk per
     (from_academic_year, to_academic_year, division).
  3. Drop grade FK + update unique_together.
"""
from django.db import migrations, models
import django.db.models.deletion


def clear_and_deduplicate(apps, schema_editor):
    # StudentFees must go first (they PROTECT FeeStructureItem → FeeStructure cascade)
    apps.get_model('fees', 'StudentFee').objects.all().delete()

    # Keep only the first (lowest pk) structure per (from_year, to_year, division)
    FeeStructure = apps.get_model('fees', 'FeeStructure')
    seen = {}
    for fs in FeeStructure.objects.order_by('id'):
        key = (fs.from_academic_year_id, fs.to_academic_year_id, fs.division_id)
        if key in seen:
            # Delete items first to avoid FK issues
            apps.get_model('fees', 'FeeStructureItem').objects.filter(structure=fs).delete()
            fs.delete()
        else:
            seen[key] = fs.pk


class Migration(migrations.Migration):
    atomic = False  # mixed RunPython + DDL on PostgreSQL

    dependencies = [
        ('fees', '0009_feestructure_item'),
    ]

    operations = [
        # ── 1. Clear data & deduplicate ───────────────────────────────────
        migrations.RunPython(clear_and_deduplicate, migrations.RunPython.noop),

        # ── 2. Drop old unique_together (includes grade) ──────────────────
        migrations.AlterUniqueTogether(
            name='feestructure',
            unique_together=set(),
        ),

        # ── 3. Remove grade FK ────────────────────────────────────────────
        migrations.RemoveField(
            model_name='feestructure',
            name='grade',
        ),

        # ── 4. Apply new unique_together (division-level) ─────────────────
        migrations.AlterUniqueTogether(
            name='feestructure',
            unique_together={('from_academic_year', 'to_academic_year', 'division')},
        ),

        # ── 5. Update ordering meta ───────────────────────────────────────
        migrations.AlterModelOptions(
            name='feestructure',
            options={'ordering': ['from_academic_year', 'division__name']},
        ),
    ]
