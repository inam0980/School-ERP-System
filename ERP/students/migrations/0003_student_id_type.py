from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_add_performance_indexes'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='id_type',
            field=models.CharField(
                choices=[
                    ('NATIONAL_ID', 'National ID / هوية وطنية'),
                    ('IQAMA',       'Iqama / إقامة'),
                    ('PASSPORT',    'Passport / جواز السفر'),
                ],
                default='NATIONAL_ID',
                max_length=15,
                verbose_name='ID Type / نوع الهوية',
                help_text='Saudi students: National ID (هوية وطنية)  ·  Residents: Iqama (إقامة)  ·  Others: Passport',
            ),
        ),
        migrations.AlterField(
            model_name='student',
            name='national_id',
            field=models.CharField(
                blank=True,
                max_length=50,
                verbose_name='ID Number / رقم الهوية',
            ),
        ),
    ]
