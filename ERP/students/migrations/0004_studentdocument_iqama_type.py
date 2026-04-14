from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0003_student_id_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentdocument',
            name='doc_type',
            field=models.CharField(
                choices=[
                    ('NATIONAL_ID',   'National ID / الهوية الوطنية'),
                    ('IQAMA',         'Iqama / إقامة'),
                    ('PASSPORT',      'Passport / جواز السفر'),
                    ('BIRTH_CERT',    'Birth Certificate / شهادة الميلاد'),
                    ('TRANSFER_CERT', 'Transfer Certificate / شهادة النقل'),
                    ('PHOTO',         'Photograph / صورة شخصية'),
                    ('OTHER',         'Other / أخرى'),
                ],
                max_length=20,
                verbose_name='Document Type / نوع الوثيقة',
            ),
        ),
    ]
