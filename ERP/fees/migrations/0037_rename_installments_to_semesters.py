"""
Rename tuition payment fee types from 'Nth Installment' to semester-based
names. The first ceil(N/2) payments of a structure fall under Semester 1,
the rest under Semester 2:

    2 payments → '1st Semester', '2nd Semester'
    3 payments → '1st Semester - 1st Installment',
                 '1st Semester - 2nd Installment',
                 '2nd Semester'

Because the same legacy FeeType row (e.g. '2nd Installment') can mean
'Semester 2' in a 2-payment structure but 'Semester 1 - 2nd Installment'
in a 3-payment structure, items are re-pointed per structure instead of
renaming the FeeType rows in place. Legacy rows are deleted once nothing
references them.
"""
from django.db import migrations

LEGACY = ['1st Installment', '2nd Installment', '3rd Installment', '4th Installment']
ORDINALS = ['1st', '2nd', '3rd', '4th']


def _semester_payment_names(n):
    cap = (n + 1) // 2
    names = []
    for i in range(n):
        sem, k, size = ('1st', i, cap) if i < cap else ('2nd', i - cap, n - cap)
        names.append(f'{sem} Semester' if size == 1
                     else f'{sem} Semester - {ORDINALS[k]} Installment')
    return names


def forwards(apps, schema_editor):
    FeeType          = apps.get_model('fees', 'FeeType')
    FeeStructure     = apps.get_model('fees', 'FeeStructure')
    FeeStructureItem = apps.get_model('fees', 'FeeStructureItem')

    def get_target(name, like):
        ft, _ = FeeType.objects.get_or_create(
            name=name, category='OTHER',
            defaults={
                'is_taxable':   like.is_taxable,
                'is_mandatory': False,
                'description':  like.description,
            },
        )
        return ft

    structure_ids = (
        FeeStructureItem.objects
        .filter(fee_type__name__in=LEGACY)
        .values_list('structure_id', flat=True)
        .distinct()
    )
    for structure in FeeStructure.objects.filter(pk__in=list(structure_ids)):
        items = list(
            FeeStructureItem.objects
            .filter(structure=structure, fee_type__name__in=LEGACY)
            .select_related('fee_type')
        )
        items.sort(key=lambda it: LEGACY.index(it.fee_type.name))
        for it, name in zip(items, _semester_payment_names(len(items))):
            if it.fee_type.name != name:
                target = get_target(name, it.fee_type)
                # unique_together (structure, fee_type): skip if a row with
                # the target type somehow already exists on this structure.
                clash = FeeStructureItem.objects.filter(
                    structure=structure, fee_type=target).exclude(pk=it.pk).exists()
                if not clash:
                    it.fee_type = target
                    it.save(update_fields=['fee_type'])

    # Remove legacy fee types nothing points to any more
    for ft in FeeType.objects.filter(name__in=LEGACY):
        if not ft.structure_items.exists():
            ft.delete()


def backwards(apps, schema_editor):
    # The legacy names are ambiguous (see module docstring) — no reverse.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('fees', '0036_payment_installment_fk'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
