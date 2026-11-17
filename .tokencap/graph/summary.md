# TokenCap Project Graph

Generated: 11/17/2026, 7:02:26 AM

> **Language Support Note**: The graph only parses JS/TS imports
> (`.js`, `.jsx`, `.ts`, `.tsx`, `.mjs`, `.cjs`). Files in other languages
> (Python, Go, Rust, etc.) appear as isolated nodes with no edges.

## Changed Files

_No changed files detected, or Git is unavailable._

## File Relationships

ERP/ERP/settings_test.py
→ ERP/ERP/settings.py

ERP/academics/admin.py
→ ERP/academics/models.py

ERP/academics/forms.py
→ ERP/academics/models.py
→ ERP/core/models.py

ERP/academics/models.py
→ ERP/core/models.py
→ ERP/students/models.py

ERP/academics/urls.py
→ ERP/academics/views.py

ERP/academics/views.py
→ ERP/accounts/decorators.py
→ ERP/students/models.py
→ ERP/core/models.py
→ ERP/academics/models.py
→ ERP/academics/forms.py

ERP/accounts/admin.py
→ ERP/accounts/models.py

ERP/accounts/management/commands/create_super_admin.py
→ ERP/accounts/models.py

ERP/accounts/urls.py
→ ERP/accounts/views.py

ERP/accounts/views.py
→ ERP/accounts/decorators.py
→ ERP/accounts/models.py

ERP/ai_features/analytics.py
→ ERP/students/models.py
→ ERP/academics/models.py
→ ERP/core/models.py
→ ERP/fees/models.py
→ ERP/attendance/models.py

ERP/ai_features/urls.py
→ ERP/ai_features/views.py

ERP/ai_features/views.py
→ ERP/accounts/decorators.py
→ ERP/core/models.py
→ ERP/students/models.py
→ ERP/ai_features/analytics.py

ERP/attendance/admin.py
→ ERP/attendance/models.py

ERP/attendance/forms.py
→ ERP/core/models.py

ERP/attendance/models.py
→ ERP/students/models.py

ERP/attendance/urls.py
→ ERP/attendance/views.py

ERP/attendance/views.py
→ ERP/accounts/decorators.py
→ ERP/students/models.py
→ ERP/core/models.py
→ ERP/attendance/models.py
→ ERP/attendance/forms.py

ERP/core/admin.py
→ ERP/core/models.py

ERP/core/forms.py
→ ERP/core/models.py

ERP/core/management/commands/seed_demo_data.py
→ ERP/accounts/models.py
→ ERP/core/models.py
→ ERP/students/models.py
→ ERP/attendance/models.py
→ ERP/academics/models.py
→ ERP/fees/models.py

ERP/core/management/commands/seed_grades.py
→ ERP/core/models.py

ERP/core/management/commands/seed_initial_data.py
→ ERP/core/models.py
→ ERP/accounts/models.py

ERP/core/management/commands/seed_students.py
→ ERP/core/models.py
→ ERP/students/models.py
→ ERP/fees/models.py
→ ERP/academics/models.py
→ ERP/attendance/models.py

ERP/core/urls.py
→ ERP/core/views.py

ERP/core/views.py
→ ERP/accounts/decorators.py
→ ERP/core/models.py
→ ERP/core/forms.py
→ ERP/students/models.py
→ ERP/attendance/models.py

ERP/fees/admin.py
→ ERP/fees/models.py

ERP/fees/forms.py
→ ERP/core/models.py
→ ERP/fees/models.py
→ ERP/accounts/models.py

ERP/fees/management/commands/recalc_student_fees.py
→ ERP/fees/models.py

ERP/fees/migrations/0001_initial.py
→ ERP/fees/models.py

ERP/fees/migrations/0026_external_candidate.py
→ ERP/fees/models.py

ERP/fees/migrations/0039_payment_is_voided_payment_void_reason_and_more.py
→ ERP/fees/models.py

ERP/fees/models.py
→ ERP/core/models.py
→ ERP/students/models.py

ERP/fees/pdf_exports.py
→ ERP/accounts/decorators.py
→ ERP/core/models.py
→ ERP/fees/models.py

ERP/fees/urls.py
→ ERP/fees/views.py

ERP/fees/views.py
→ ERP/accounts/decorators.py
→ ERP/students/models.py
→ ERP/core/models.py
→ ERP/fees/models.py
→ ERP/fees/forms.py
→ ERP/fees/pdf_exports.py

ERP/serve.py
→ ERP/ERP/wsgi.py

ERP/staff/admin.py
→ ERP/staff/models.py

ERP/staff/forms.py
→ ERP/core/models.py
→ ERP/staff/models.py

ERP/staff/models.py
→ ERP/core/models.py

ERP/staff/urls.py
→ ERP/staff/views.py

ERP/staff/views.py
→ ERP/accounts/decorators.py
→ ERP/accounts/models.py
→ ERP/attendance/models.py
→ ERP/academics/models.py
→ ERP/core/models.py
→ ERP/students/models.py
→ ERP/staff/models.py
→ ERP/staff/forms.py

ERP/students/admin.py
→ ERP/students/models.py

ERP/students/forms.py
→ ERP/core/models.py
→ ERP/students/models.py

ERP/students/migrations/0001_initial.py
→ ERP/students/models.py

ERP/students/models.py
→ ERP/core/models.py

ERP/students/urls.py
→ ERP/students/views.py

ERP/students/views.py
→ ERP/accounts/decorators.py
→ ERP/students/models.py
→ ERP/students/forms.py
→ ERP/fees/models.py
→ ERP/core/models.py

ERP/tests/conftest.py
→ ERP/accounts/models.py
→ ERP/tests/__init__.py
→ ERP/tests/factories.py

ERP/tests/factories.py
→ ERP/accounts/models.py
→ ERP/core/models.py
→ ERP/students/models.py
→ ERP/attendance/models.py
→ ERP/academics/models.py
→ ERP/fees/models.py
→ ERP/staff/models.py

ERP/tests/integration/test_auth.py
→ ERP/accounts/models.py
→ ERP/tests/factories.py

ERP/tests/integration/test_fees.py
→ ERP/accounts/models.py
→ ERP/fees/models.py
→ ERP/tests/factories.py

ERP/tests/integration/test_marks.py
→ ERP/accounts/models.py
→ ERP/academics/models.py
→ ERP/tests/factories.py

ERP/tests/integration/test_students.py
→ ERP/accounts/models.py
→ ERP/students/models.py
→ ERP/tests/factories.py

backfill_missing.py
→ ERP/students/models.py
→ ERP/core/models.py

deploy/fix_service/serve.py
→ ERP/ERP/wsgi.py

gen_students.py
→ ERP/core/models.py

## Important Nodes

- ERP/tests/__init__.py — test
- ERP/tests/conftest.py — test
- ERP/tests/factories.py — test
- ERP/tests/integration/__init__.py — test
- ERP/tests/integration/test_auth.py — test
- ERP/tests/integration/test_fees.py — test
- ERP/tests/integration/test_marks.py — test
- ERP/tests/integration/test_students.py — test
- ERP/tests/unit/__init__.py — test
- ERP/academics/migrations/__init__.py — database
- ERP/academics/migrations/0001_initial.py — database
- ERP/accounts/migrations/__init__.py — database
- ERP/accounts/migrations/0001_initial.py — database
- ERP/ai_features/migrations/__init__.py — database
- ERP/attendance/migrations/__init__.py — database
- ERP/attendance/migrations/0001_initial.py — database
- ERP/attendance/migrations/0002_add_performance_indexes.py — database
- ERP/core/management/commands/seed_demo_data.py — database
- ERP/core/management/commands/seed_grades.py — database
- ERP/core/management/commands/seed_initial_data.py — database
- ERP/core/management/commands/seed_students.py — database
- ERP/core/migrations/__init__.py — database
- ERP/core/migrations/0001_initial.py — database
- ERP/core/migrations/0002_add_home_study_division.py — database
- ERP/core/migrations/0003_board.py — database
- ERP/core/migrations/0004_alter_division_name.py — database
- ERP/core/migrations/0005_add_default_divisions_grades_sections.py — database
- ERP/core/migrations/0006_fix_default_grades.py — database
- ERP/core/migrations/0007_studymode.py — database
- ERP/fees/migrations/__init__.py — database
- ERP/fees/migrations/0001_initial.py — database
- ERP/fees/migrations/0002_add_performance_indexes.py — database
- ERP/fees/migrations/0003_fees_invoice_creditnote_bankverify.py — database
- ERP/fees/migrations/0004_add_fee_categories.py — database
- ERP/fees/migrations/0005_tuition_fee_config.py — database
- ERP/fees/migrations/0006_payment_plan.py — database
- ERP/fees/migrations/0007_fee_structure_bundle.py — database
- ERP/fees/migrations/0008_feestructure_year_range.py — database
- ERP/fees/migrations/0009_feestructure_item.py — database
- ERP/fees/migrations/0010_remove_grade_from_feestructure.py — database
- ERP/fees/migrations/0011_feestructure_grade_academic_year.py — database
- ERP/fees/migrations/0012_payment_mode_credit_bank_installment.py — database
- ERP/fees/migrations/0013_feetype_default_amount.py — database
- ERP/fees/migrations/0014_add_feetype_is_mandatory.py — database
- ERP/fees/migrations/0015_mark_mandatory_fee_types.py — database
- ERP/fees/migrations/0016_add_feetype_fixed_down_payment.py — database
- ERP/fees/migrations/0017_add_feestructure_min_down_payment.py — database
- ERP/fees/migrations/0018_replace_due_date_with_four_dates.py — database
- ERP/fees/migrations/0019_revert_to_single_due_date.py — database
- ERP/fees/migrations/0020_add_structure_type_to_bundle.py — database
- ERP/fees/migrations/0021_add_code_to_bundle.py — database
- ERP/fees/migrations/0022_add_creditnote_fields_to_taxinvoice.py — database
- ERP/fees/migrations/0023_remove_fee_structure_bundle.py — database
- ERP/fees/migrations/0024_add_structure_type_to_feestructure.py — database
- ERP/fees/migrations/0025_add_other_structure_type.py — database
- ERP/fees/migrations/0026_external_candidate.py — database
- ERP/fees/migrations/0027_external_candidate_board.py — database
- ERP/fees/migrations/0028_externalcandidate_enrolled_student_and_more.py — database
- ERP/fees/migrations/0029_alter_externalcandidate_board.py — database
- ERP/fees/migrations/0030_add_division_to_external_candidate.py — database
- ERP/fees/migrations/0031_externalcandidate_is_saudi.py — database
- ERP/fees/migrations/0032_alter_feestructure_structure_type.py — database
- ERP/fees/migrations/0033_alter_feestructure_unique_together_and_more.py — database
- ERP/fees/migrations/0034_invoice_first_printed_at.py — database
- ERP/fees/migrations/0035_payment_plan_semester.py — database
- ERP/fees/migrations/0036_payment_installment_fk.py — database
- ERP/fees/migrations/0037_rename_installments_to_semesters.py — database
- ERP/fees/migrations/0038_alter_tuitionfeeconfig_num_payments_and_more.py — database
- ERP/fees/migrations/0039_payment_is_voided_payment_void_reason_and_more.py — database
- ERP/staff/migrations/__init__.py — database
- ERP/staff/migrations/0001_initial.py — database
- ERP/students/migrations/__init__.py — database
- ERP/students/migrations/0001_initial.py — database
- ERP/students/migrations/0002_add_performance_indexes.py — database
- ERP/students/migrations/0003_student_id_type.py — database
- ERP/students/migrations/0004_studentdocument_iqama_type.py — database
- ERP/students/migrations/0005_add_father_national_id.py — database
- ERP/students/migrations/0006_add_father_mother_detail_fields.py — database
- ERP/students/migrations/0007_add_sibling_model.py — database
- ERP/students/migrations/0008_add_iqama_passport_religion_birthplace.py — database
- ERP/students/migrations/0009_add_authorized_pickup.py — database
- ERP/students/migrations/0010_add_fee_category.py — database
- ERP/students/migrations/0011_alter_student_enrollment_type.py — database
- ERP/students/migrations/0012_student_study_mode.py — database
- ERP/students/migrations/0013_alter_student_fee_category.py — database
- ERP/students/migrations/0014_religion_choices.py — database
- ERP/students/migrations/0015_promotionhistory.py — database
- ERP/students/migrations/0016_student_fees_contact_email_and_more.py — database
- ERP/theme/static_src/postcss.config.js — config
- ERP/theme/static_src/tailwind.config.js — config
- tailwind.config.js — config

## All Scanned Files

Total: 186 JS/TS files scanned.

### 🗄️ Database (79)

- ERP/academics/migrations/__init__.py
- ERP/academics/migrations/0001_initial.py
- ERP/accounts/migrations/__init__.py
- ERP/accounts/migrations/0001_initial.py
- ERP/ai_features/migrations/__init__.py
- ERP/attendance/migrations/__init__.py
- ERP/attendance/migrations/0001_initial.py
- ERP/attendance/migrations/0002_add_performance_indexes.py
- ERP/core/management/commands/seed_demo_data.py
- ERP/core/management/commands/seed_grades.py
- ERP/core/management/commands/seed_initial_data.py
- ERP/core/management/commands/seed_students.py
- ERP/core/migrations/__init__.py
- ERP/core/migrations/0001_initial.py
- ERP/core/migrations/0002_add_home_study_division.py
- ERP/core/migrations/0003_board.py
- ERP/core/migrations/0004_alter_division_name.py
- ERP/core/migrations/0005_add_default_divisions_grades_sections.py
- ERP/core/migrations/0006_fix_default_grades.py
- ERP/core/migrations/0007_studymode.py
- ERP/fees/migrations/__init__.py
- ERP/fees/migrations/0001_initial.py
- ERP/fees/migrations/0002_add_performance_indexes.py
- ERP/fees/migrations/0003_fees_invoice_creditnote_bankverify.py
- ERP/fees/migrations/0004_add_fee_categories.py
- ERP/fees/migrations/0005_tuition_fee_config.py
- ERP/fees/migrations/0006_payment_plan.py
- ERP/fees/migrations/0007_fee_structure_bundle.py
- ERP/fees/migrations/0008_feestructure_year_range.py
- ERP/fees/migrations/0009_feestructure_item.py
- ERP/fees/migrations/0010_remove_grade_from_feestructure.py
- ERP/fees/migrations/0011_feestructure_grade_academic_year.py
- ERP/fees/migrations/0012_payment_mode_credit_bank_installment.py
- ERP/fees/migrations/0013_feetype_default_amount.py
- ERP/fees/migrations/0014_add_feetype_is_mandatory.py
- ERP/fees/migrations/0015_mark_mandatory_fee_types.py
- ERP/fees/migrations/0016_add_feetype_fixed_down_payment.py
- ERP/fees/migrations/0017_add_feestructure_min_down_payment.py
- ERP/fees/migrations/0018_replace_due_date_with_four_dates.py
- ERP/fees/migrations/0019_revert_to_single_due_date.py
- ERP/fees/migrations/0020_add_structure_type_to_bundle.py
- ERP/fees/migrations/0021_add_code_to_bundle.py
- ERP/fees/migrations/0022_add_creditnote_fields_to_taxinvoice.py
- ERP/fees/migrations/0023_remove_fee_structure_bundle.py
- ERP/fees/migrations/0024_add_structure_type_to_feestructure.py
- ERP/fees/migrations/0025_add_other_structure_type.py
- ERP/fees/migrations/0026_external_candidate.py
- ERP/fees/migrations/0027_external_candidate_board.py
- ERP/fees/migrations/0028_externalcandidate_enrolled_student_and_more.py
- ERP/fees/migrations/0029_alter_externalcandidate_board.py
- ERP/fees/migrations/0030_add_division_to_external_candidate.py
- ERP/fees/migrations/0031_externalcandidate_is_saudi.py
- ERP/fees/migrations/0032_alter_feestructure_structure_type.py
- ERP/fees/migrations/0033_alter_feestructure_unique_together_and_more.py
- ERP/fees/migrations/0034_invoice_first_printed_at.py
- ERP/fees/migrations/0035_payment_plan_semester.py
- ERP/fees/migrations/0036_payment_installment_fk.py
- ERP/fees/migrations/0037_rename_installments_to_semesters.py
- ERP/fees/migrations/0038_alter_tuitionfeeconfig_num_payments_and_more.py
- ERP/fees/migrations/0039_payment_is_voided_payment_void_reason_and_more.py
- ERP/staff/migrations/__init__.py
- ERP/staff/migrations/0001_initial.py
- ERP/students/migrations/__init__.py
- ERP/students/migrations/0001_initial.py
- ERP/students/migrations/0002_add_performance_indexes.py
- ERP/students/migrations/0003_student_id_type.py
- ERP/students/migrations/0004_studentdocument_iqama_type.py
- ERP/students/migrations/0005_add_father_national_id.py
- ERP/students/migrations/0006_add_father_mother_detail_fields.py
- ERP/students/migrations/0007_add_sibling_model.py
- ERP/students/migrations/0008_add_iqama_passport_religion_birthplace.py
- ERP/students/migrations/0009_add_authorized_pickup.py
- ERP/students/migrations/0010_add_fee_category.py
- ERP/students/migrations/0011_alter_student_enrollment_type.py
- ERP/students/migrations/0012_student_study_mode.py
- ERP/students/migrations/0013_alter_student_fee_category.py
- ERP/students/migrations/0014_religion_choices.py
- ERP/students/migrations/0015_promotionhistory.py
- ERP/students/migrations/0016_student_fees_contact_email_and_more.py

### 🔧 Config (3)

- ERP/theme/static_src/postcss.config.js
- ERP/theme/static_src/tailwind.config.js
- tailwind.config.js

### 📄 Unknown (95)

- backfill_missing.py
- deploy/fix_service/serve.py
- deploy/fix_static/settings.py
- deploy/fix_static/tailwind.js
- deploy/fix_static/urls.py
- ERP/academics/__init__.py
- ERP/academics/admin.py
- ERP/academics/apps.py
- ERP/academics/forms.py
- ERP/academics/models.py
- ERP/academics/tests.py
- ERP/academics/urls.py
- ERP/academics/views.py
- ERP/accounts/__init__.py
- ERP/accounts/admin.py
- ERP/accounts/apps.py
- ERP/accounts/decorators.py
- ERP/accounts/management/__init__.py
- ERP/accounts/management/commands/__init__.py
- ERP/accounts/management/commands/create_super_admin.py
- ERP/accounts/models.py
- ERP/accounts/tests.py
- ERP/accounts/urls.py
- ERP/accounts/views.py
- ERP/ai_features/__init__.py
- ERP/ai_features/admin.py
- ERP/ai_features/analytics.py
- ERP/ai_features/apps.py
- ERP/ai_features/models.py
- ERP/ai_features/tests.py
- ERP/ai_features/urls.py
- ERP/ai_features/views.py
- ERP/attendance/__init__.py
- ERP/attendance/admin.py
- ERP/attendance/apps.py
- ERP/attendance/forms.py
- ERP/attendance/models.py
- ERP/attendance/urls.py
- ERP/attendance/views.py
- ERP/core/__init__.py
- ERP/core/admin.py
- ERP/core/apps.py
- ERP/core/forms.py
- ERP/core/management/__init__.py
- ERP/core/management/commands/__init__.py
- ERP/core/models.py
- ERP/core/tests.py
- ERP/core/urls.py
- ERP/core/views.py
- ERP/ERP/__init__.py
- ERP/ERP/asgi.py
- ERP/ERP/settings_production.py
- ERP/ERP/settings_test.py
- ERP/ERP/settings.py
- ERP/ERP/urls.py
- ERP/ERP/wsgi.py
- ERP/fees/__init__.py
- ERP/fees/admin.py
- ERP/fees/apps.py
- ERP/fees/forms.py
- ERP/fees/management/__init__.py
- ERP/fees/management/commands/__init__.py
- ERP/fees/management/commands/recalc_student_fees.py
- ERP/fees/models.py
- ERP/fees/pdf_exports.py
- ERP/fees/templatetags/__init__.py
- ERP/fees/templatetags/fee_pdf_filters.py
- ERP/fees/tests.py
- ERP/fees/urls.py
- ERP/fees/views.py
- ERP/manage.py
- ERP/serve.py
- ERP/staff/__init__.py
- ERP/staff/admin.py
- ERP/staff/apps.py
- ERP/staff/forms.py
- ERP/staff/models.py
- ERP/staff/tests.py
- ERP/staff/urls.py
- ERP/staff/views.py
- ERP/static/js/tailwind.js
- ERP/students/__init__.py
- ERP/students/admin.py
- ERP/students/apps.py
- ERP/students/forms.py
- ERP/students/models.py
- ERP/students/tests.py
- ERP/students/urls.py
- ERP/students/views.py
- ERP/templatetags/__init__.py
- ERP/templatetags/fee_pdf_filters.py
- ERP/theme/__init__.py
- ERP/theme/apps.py
- gen_students.py
- gunicorn.conf.py
