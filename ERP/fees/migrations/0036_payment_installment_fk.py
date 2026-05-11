from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fees', '0035_payment_plan_semester'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='installment',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=models.SET_NULL,
                related_name='payments',
                to='fees.paymentplaninstallment',
                help_text='Set if this payment is allocated to a specific installment.',
            ),
        ),
    ]
