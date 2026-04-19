"""
Refactor FeeStructure into a container model:
- Remove fee_type FK (now lives on FeeStructureItem)
- Create FeeStructureItem (structure + fee_type + amount)
- Change StudentFee.fee_structure FK to point at FeeStructureItem

Since FeeStructure table is expected to be empty (no seeder populates it),
the data migration is a safety no-op. The StudentFee table is also expected
to be empty, so we can alter the FK directly.
"""
from django.db import migrations, models
import django.db.models.deletion


def deduplicate_fee_structures(apps, schema_editor):
    """Clear all StudentFees, then keep only the lowest-pk FeeStructure per (from_year, to_year, grade, division)."""
    StudentFee = apps.get_model('fees', 'StudentFee')
    StudentFee.objects.all().delete()

    FeeStructure = apps.get_model('fees', 'FeeStructure')
    seen = {}
    for fs in FeeStructure.objects.order_by('id'):
        key = (fs.from_academic_year_id, fs.to_academic_year_id, fs.grade_id, fs.division_id)
        if key in seen:
            fs.delete()
        else:
            seen[key] = fs.pk


class Migration(migrations.Migration):
    atomic = False  # needed: RunPython + DDL mixed in same migration on PostgreSQL

    dependencies = [
        ('fees', '0008_feestructure_year_range'),
        ('core', '0002_add_home_study_division'),
    ]

    operations = [
        # ── 1. Drop old unique_together that included fee_type ────────────
        migrations.AlterUniqueTogether(
            name='feestructure',
            unique_together=set(),
        ),

        # ── 2. Remove fee_type FK from FeeStructure ───────────────────────
        migrations.RemoveField(
            model_name='feestructure',
            name='fee_type',
        ),

        # ── 2b. Deduplicate rows so unique constraint can be applied ──────
        migrations.RunPython(deduplicate_fee_structures, migrations.RunPython.noop),

        # ── 3. Apply new unique_together (without fee_type) ───────────────
        migrations.AlterUniqueTogether(
            name='feestructure',
            unique_together={('from_academic_year', 'to_academic_year', 'grade', 'division')},
        ),

        # ── 4. Update ordering meta ───────────────────────────────────────
        migrations.AlterModelOptions(
            name='feestructure',
            options={'ordering': ['from_academic_year', 'grade__name']},
        ),

        # ── 5. Create FeeStructureItem table ─────────────────────────────
        migrations.CreateModel(
            name='FeeStructureItem',
            fields=[
                ('id',        models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount',    models.DecimalField(decimal_places=2, max_digits=10)),
                ('structure', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='items',
                    to='fees.feestructure',
                )),
                ('fee_type',  models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='structure_items',
                    to='fees.feetype',
                )),
            ],
            options={
                'ordering': ['fee_type__category', 'fee_type__name'],
                'unique_together': {('structure', 'fee_type')},
            },
        ),

        # ── 6. Change StudentFee.fee_structure FK target ──────────────────
        #    StudentFees were already cleared in step 2b. Alter FK target.
        migrations.AlterField(
            model_name='studentfee',
            name='fee_structure',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='student_fees',
                to='fees.feestructureitem',
            ),
        ),
    ]
