"""
Migration 0011 — Redesign FeeStructure:
  • Replace from_academic_year + to_academic_year  →  single academic_year
  • Replace division FK  →  grade FK (division is derived from grade.division)
  • unique_together: (academic_year, grade)

Because the field set changes completely, we clear all FeeStructure rows first
(and their items + any StudentFees that reference those items) to avoid
constraint violations.  This is safe for a dev/fresh-data environment.
"""
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    atomic = False

    dependencies = [
        ('fees', '0010_remove_grade_from_feestructure'),
        ('core', '0001_initial'),
    ]

    operations = [
        # 1. Wipe dependant data before schema surgery
        migrations.RunSQL(
            "DELETE FROM fees_studentfee;",
            reverse_sql=migrations.RunSQL.noop,
        ),
        migrations.RunSQL(
            "DELETE FROM fees_feestructureitem;",
            reverse_sql=migrations.RunSQL.noop,
        ),
        migrations.RunSQL(
            "DELETE FROM fees_feestructure;",
            reverse_sql=migrations.RunSQL.noop,
        ),

        # 2. Drop old unique_together so we can drop columns freely
        migrations.AlterUniqueTogether(
            name='feestructure',
            unique_together=set(),
        ),

        # 3. Remove old FK columns
        migrations.RemoveField(model_name='feestructure', name='from_academic_year'),
        migrations.RemoveField(model_name='feestructure', name='to_academic_year'),
        migrations.RemoveField(model_name='feestructure', name='division'),

        # 4. Add new FK columns (nullable first so DB accepts the alter)
        migrations.AddField(
            model_name='feestructure',
            name='academic_year',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='fee_structures',
                to='core.academicyear',
                verbose_name='Academic Year',
            ),
        ),
        migrations.AddField(
            model_name='feestructure',
            name='grade',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='fee_structures',
                to='core.grade',
                verbose_name='Grade',
            ),
        ),

        # 5. Make them non-nullable now that the table is empty
        migrations.AlterField(
            model_name='feestructure',
            name='academic_year',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='fee_structures',
                to='core.academicyear',
                verbose_name='Academic Year',
            ),
        ),
        migrations.AlterField(
            model_name='feestructure',
            name='grade',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='fee_structures',
                to='core.grade',
                verbose_name='Grade',
            ),
        ),

        # 6. Restore unique_together on new columns
        migrations.AlterUniqueTogether(
            name='feestructure',
            unique_together={('academic_year', 'grade')},
        ),

        # 7. Fix ordering
        migrations.AlterModelOptions(
            name='feestructure',
            options={
                'ordering': ['academic_year', 'grade__division__name', 'grade__order', 'grade__name'],
            },
        ),
    ]
