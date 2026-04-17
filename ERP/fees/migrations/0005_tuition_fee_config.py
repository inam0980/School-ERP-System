# Generated manually on 2026-04-17

import django.db.models.deletion
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fees', '0004_add_fee_categories'),
        ('core', '0002_add_home_study_division'),
    ]

    operations = [
        # ── TuitionFeeConfig ──────────────────────────────────────
        migrations.CreateModel(
            name='TuitionFeeConfig',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('structure_type', models.CharField(
                    choices=[('REGULAR', 'Regular'), ('SPECIAL', 'Special / New Students')],
                    default='REGULAR', max_length=10)),
                ('num_payments', models.PositiveSmallIntegerField(
                    choices=[(2, '2 Installments'), (3, '3 Installments')],
                    default=2, verbose_name='Number of Installments')),
                ('includes_books', models.BooleanField(
                    default=False, help_text='Tuition fee includes books')),
                ('entrance_exam_fee', models.DecimalField(
                    decimal_places=2, default=Decimal('0.00'),
                    max_digits=10, verbose_name='Entrance Exam Fee (SAR)')),
                ('registration_fee', models.DecimalField(
                    decimal_places=2, default=Decimal('0.00'),
                    max_digits=10, verbose_name='Registration Fee (SAR)')),
                ('reservation_fee', models.DecimalField(
                    decimal_places=2, default=Decimal('0.00'),
                    help_text='Down payment / حجز مقعد',
                    max_digits=10, verbose_name='Reservation / Down Payment (SAR)')),
                ('gross_tuition_fee', models.DecimalField(
                    decimal_places=2, max_digits=10,
                    verbose_name='Gross Tuition Fee (SAR)')),
                ('group_discount_enabled', models.BooleanField(default=False)),
                ('group_discount_pct', models.DecimalField(
                    decimal_places=2, default=Decimal('0.00'),
                    help_text='Discount percentage (e.g. 10 for 10%)',
                    max_digits=5, verbose_name='Group Discount (%)')),
                ('vat_pct', models.DecimalField(
                    decimal_places=2, default=Decimal('15.00'),
                    help_text='VAT rate (%) applied to non-Saudi students',
                    max_digits=5, verbose_name='VAT Rate (%)')),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('academic_year', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='tuition_configs',
                    to='core.academicyear')),
                ('division', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='tuition_configs',
                    to='core.division')),
                ('grade', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='tuition_configs',
                    to='core.grade')),
                ('from_academic_year', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='tuition_configs_from',
                    to='core.academicyear',
                    verbose_name='Applicable From Year')),
                ('to_academic_year', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='tuition_configs_to',
                    to='core.academicyear',
                    verbose_name='Applicable To Year')),
            ],
            options={
                'verbose_name': 'Tuition Fee Configuration',
                'verbose_name_plural': 'Tuition Fee Configurations',
                'ordering': ['division__name', 'grade__order', 'grade__name', 'structure_type'],
                'unique_together': {('academic_year', 'division', 'grade', 'structure_type')},
            },
        ),

        # ── TuitionInstallment ────────────────────────────────────
        migrations.CreateModel(
            name='TuitionInstallment',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('installment_type', models.CharField(
                    choices=[
                        ('RESERVATION', 'Reservation / Down Payment'),
                        ('FIRST',       '1st Installment'),
                        ('SECOND',      '2nd Installment'),
                        ('THIRD',       '3rd Installment'),
                    ],
                    max_length=15)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('due_date', models.DateField(blank=True, null=True)),
                ('notes', models.CharField(blank=True, max_length=200)),
                ('config', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='installments',
                    to='fees.tuitionfeeconfig')),
            ],
            options={
                'verbose_name': 'Tuition Installment',
                'verbose_name_plural': 'Tuition Installments',
                'ordering': ['config', 'installment_type'],
                'unique_together': {('config', 'installment_type')},
            },
        ),
    ]
