# Generated manually on 2026-04-17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='division',
            name='name',
            field=models.CharField(
                choices=[
                    ('AMERICAN',   'American'),
                    ('BRITISH',    'British'),
                    ('FRENCH',     'French'),
                    ('HOME_STUDY', 'Home Study'),
                ],
                max_length=20,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name='division',
            name='curriculum_type',
            field=models.CharField(
                choices=[
                    ('AMERICAN',   'American Common Core'),
                    ('BRITISH',    'British National Curriculum'),
                    ('FRENCH',     'French National Curriculum'),
                    ('HOME_STUDY', 'Home Study Programme'),
                ],
                max_length=20,
            ),
        ),
    ]
