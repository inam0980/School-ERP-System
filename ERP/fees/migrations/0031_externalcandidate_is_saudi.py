from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fees', '0030_add_division_to_external_candidate'),
    ]

    operations = [
        migrations.AddField(
            model_name='externalcandidate',
            name='is_saudi',
            field=models.BooleanField(
                blank=True,
                null=True,
                verbose_name='Saudi National / مواطن سعودي',
                help_text='True = Saudi (0% VAT), False/None = Non-Saudi (15% VAT on taxable fees)',
            ),
        ),
    ]
