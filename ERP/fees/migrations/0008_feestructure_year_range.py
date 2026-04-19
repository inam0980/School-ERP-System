"""
Replace FeeStructure.academic_year (single year) with
from_academic_year + to_academic_year, and drop the
amount and due_date fields (those now live on StudentFee only).
"""
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fees', '0007_fee_structure_bundle'),
        ('core', '0002_add_home_study_division'),
    ]

    operations = [
        # ── 1. Add new nullable FK columns ──────────────────────────────
        migrations.AddField(
            model_name='feestructure',
            name='from_academic_year',
            field=models.ForeignKey(
                null=True, blank=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='fee_structures_from',
                to='core.academicyear',
                verbose_name='From Academic Year',
            ),
        ),
        migrations.AddField(
            model_name='feestructure',
            name='to_academic_year',
            field=models.ForeignKey(
                null=True, blank=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='fee_structures_to',
                to='core.academicyear',
                verbose_name='To Academic Year',
            ),
        ),

        # ── 2. Copy existing academic_year into both new columns ─────────
        migrations.RunSQL(
            sql="""
                UPDATE fees_feestructure
                SET from_academic_year_id = academic_year_id,
                    to_academic_year_id   = academic_year_id
                WHERE academic_year_id IS NOT NULL;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),

        # ── 3. Make the new FK columns non-nullable ──────────────────────
        migrations.AlterField(
            model_name='feestructure',
            name='from_academic_year',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='fee_structures_from',
                to='core.academicyear',
                verbose_name='From Academic Year',
            ),
        ),
        migrations.AlterField(
            model_name='feestructure',
            name='to_academic_year',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='fee_structures_to',
                to='core.academicyear',
                verbose_name='To Academic Year',
            ),
        ),

        # ── 4. Drop the old unique_together before removing fields ───────
        migrations.AlterUniqueTogether(
            name='feestructure',
            unique_together=set(),
        ),

        # ── 5. Remove the old columns ────────────────────────────────────
        migrations.RemoveField(model_name='feestructure', name='academic_year'),
        migrations.RemoveField(model_name='feestructure', name='amount'),
        migrations.RemoveField(model_name='feestructure', name='due_date'),

        # ── 6. Apply the new unique_together ─────────────────────────────
        migrations.AlterUniqueTogether(
            name='feestructure',
            unique_together={('from_academic_year', 'to_academic_year', 'grade', 'division', 'fee_type')},
        ),

        # ── 7. Update ordering meta ──────────────────────────────────────
        migrations.AlterModelOptions(
            name='feestructure',
            options={'ordering': ['from_academic_year', 'grade__name', 'fee_type__name']},
        ),
    ]
