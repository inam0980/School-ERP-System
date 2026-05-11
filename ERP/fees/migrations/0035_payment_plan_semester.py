from django.db import migrations, models


def wipe_existing_payment_plans(apps, schema_editor):
    """Delete all existing PaymentPlan records so they can be re-set up
    under the new semester-aware logic."""
    PaymentPlan = apps.get_model('fees', 'PaymentPlan')
    PaymentPlan.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('fees', '0034_invoice_first_printed_at'),
    ]

    operations = [
        migrations.RunPython(wipe_existing_payment_plans, migrations.RunPython.noop),
        migrations.AddField(
            model_name='paymentplaninstallment',
            name='semester',
            field=models.PositiveSmallIntegerField(
                choices=[(1, 'Semester 1'), (2, 'Semester 2')],
                default=1,
                help_text='Which semester this installment belongs to (1 or 2).',
            ),
        ),
    ]
