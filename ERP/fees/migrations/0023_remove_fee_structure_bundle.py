from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fees', '0022_add_creditnote_fields_to_taxinvoice'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BundleInstallment',
        ),
        migrations.DeleteModel(
            name='FeeStructureBundle',
        ),
    ]
