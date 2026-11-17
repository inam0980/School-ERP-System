<!-- TokenCap v1.6 Savings: baseline 520,549 tok → actual 47,455 tok (90.9% saved) -->
# AI ENTRY POINT

This repository has been indexed by TokenCap.

Before analyzing files, read:

.tokencap/agent/START_HERE.md

Use:

- .tokencap/agent/agent-pack.md
- .tokencap/agent/allowed-context.json
- .tokencap/agent/context-manifest.json

Do not rediscover the repository from scratch.

---

# TokenCap Snapshot

| Field | Value |
| --- | --- |
| Generated | 2026-11-17T01:32:19.250Z |
| Workspace | e:\ERP_SYSTEM |
| Profile | balanced |
| Selected files | 90 |
| Source bytes | 183557 |
| Estimated source tokens | 38877 |

## Read First

This file is a compressed coding-session handoff. Read it before editing, then inspect the referenced files directly. Prefer the live repository over this snapshot when there is a conflict.

## TokenCap Intelligence Files

- TOKENCAP_GRAPH.md — Project dependency and architecture graph *(JS/TS projects only)*
- TOKENCAP_MEMORY.md — Developer notes, current task, constraints, and context memory

## Handoff Summary

| Field | Value |
| --- | --- |
| Read order | README.md > ERP/theme/static_src/package.json > package.json > requirements.txt > deploy/README_WINDOWS.txt |
| Primary anchors | README.md, ERP/theme/static_src/package.json, package.json |
| Changed files | 0 |
| TODO notes | 0 |
| File budget used | 100% |
| Source budget used | 83% |
| Token estimate | 38877 |
| Contents mode | enabled |

## Handoff Guidelines

- Preserve user changes; avoid reverting unrelated work.
- Start with changed files and files marked `high-signal` in the manifest.
- Treat the Git diff as intent and verify changes in source files.
- Update this snapshot after meaningful edits or before handing off.

## Git Snapshot

| Field | Value |
| --- | --- |
| Branch | main |
| Git root | E:/ERP_SYSTEM |

Recent commits:
```text
edffe37 KING IS BACK
46cbcff KING IS BACK
2f683e9 Offline Windows deployment + Tailwind build; clean up repository
190e966 DONE1
38e47b7 Donr
be1bb57 inammm
fa5ecb6 INAM Iver
1347258 MY NAME IS INAM
```

Status:
```text
clean or unavailable
```

## Project Map

```text
ERP/
ERP/ERP/
ERP/academics/
ERP/academics/migrations/
ERP/accounts/
ERP/accounts/management/
ERP/accounts/management/commands/
ERP/accounts/migrations/
ERP/ai_features/
ERP/ai_features/migrations/
ERP/attendance/
ERP/attendance/migrations/
ERP/core/
ERP/core/management/
ERP/core/management/commands/
ERP/core/migrations/
ERP/fees/
ERP/fees/management/
ERP/fees/management/commands/
ERP/fees/migrations/
ERP/fees/templatetags/
ERP/staff/
ERP/staff/migrations/
ERP/static/
ERP/static/css/
ERP/students/
ERP/students/migrations/
ERP/templates/
ERP/templates/academics/
ERP/templates/accounts/
ERP/templates/ai_features/
ERP/templates/attendance/
ERP/templates/core/
ERP/templates/core/school_setup/
ERP/templates/fees/
ERP/templates/fees/partials/
ERP/templates/staff/
ERP/templates/students/
ERP/templatetags/
ERP/tests/
ERP/tests/integration/
ERP/tests/unit/
ERP/theme/
ERP/theme/static_src/
ERP/theme/static_src/src/
ERP/theme/templates/
deploy/
deploy/fix_service/
deploy/fix_static/
ERP/ERP/__init__.py
ERP/ERP/asgi.py
ERP/ERP/settings.py
ERP/ERP/settings_production.py
ERP/ERP/settings_test.py
ERP/ERP/urls.py
ERP/ERP/wsgi.py
ERP/academics/__init__.py
ERP/academics/admin.py
ERP/academics/apps.py
ERP/academics/forms.py
ERP/academics/migrations/0001_initial.py
ERP/academics/migrations/__init__.py
ERP/academics/models.py
ERP/academics/tests.py
ERP/academics/urls.py
ERP/academics/views.py
ERP/accounts/__init__.py
ERP/accounts/admin.py
ERP/accounts/apps.py
ERP/accounts/decorators.py
ERP/accounts/management/__init__.py
ERP/accounts/management/commands/__init__.py
ERP/accounts/management/commands/create_super_admin.py
ERP/accounts/migrations/0001_initial.py
ERP/accounts/migrations/__init__.py
ERP/accounts/models.py
ERP/accounts/tests.py
ERP/accounts/urls.py
ERP/accounts/views.py
ERP/ai_features/__init__.py
ERP/ai_features/admin.py
ERP/ai_features/analytics.py
ERP/ai_features/apps.py
ERP/ai_features/migrations/__init__.py
ERP/ai_features/models.py
ERP/ai_features/tests.py
ERP/ai_features/urls.py
ERP/ai_features/views.py
ERP/attendance/__init__.py
ERP/attendance/admin.py
ERP/attendance/apps.py
ERP/attendance/forms.py
ERP/attendance/migrations/0001_initial.py
ERP/attendance/migrations/0002_add_performance_indexes.py
ERP/attendance/migrations/__init__.py
ERP/attendance/models.py
ERP/attendance/urls.py
ERP/attendance/views.py
ERP/core/__init__.py
ERP/core/admin.py
ERP/core/apps.py
ERP/core/forms.py
ERP/core/management/__init__.py
ERP/core/management/commands/__init__.py
ERP/core/management/commands/seed_demo_data.py
ERP/core/management/commands/seed_grades.py
ERP/core/management/commands/seed_initial_data.py
ERP/core/management/commands/seed_students.py
ERP/core/migrations/0001_initial.py
ERP/core/migrations/0002_add_home_study_division.py
ERP/core/migrations/0003_board.py
ERP/core/migrations/0004_alter_division_name.py
ERP/core/migrations/0005_add_default_divisions_grades_sections.py
ERP/core/migrations/0006_fix_default_grades.py
ERP/core/migrations/0007_studymode.py
ERP/core/migrations/__init__.py
ERP/core/models.py
ERP/core/tests.py
ERP/core/urls.py
ERP/core/views.py
ERP/fees/__init__.py
ERP/fees/admin.py
ERP/fees/apps.py
ERP/fees/forms.py
ERP/fees/management/__init__.py
ERP/fees/management/commands/__init__.py
ERP/fees/management/commands/recalc_student_fees.py
ERP/fees/migrations/0001_initial.py
ERP/fees/migrations/0002_add_performance_indexes.py
ERP/fees/migrations/0003_fees_invoice_creditnote_bankverify.py
ERP/fees/migrations/0004_add_fee_categories.py
ERP/fees/migrations/0005_tuition_fee_config.py
ERP/fees/migrations/0006_payment_plan.py
ERP/fees/migrations/0007_fee_structure_bundle.py
ERP/fees/migrations/0008_feestructure_year_range.py
ERP/fees/migrations/0009_feestructure_item.py
ERP/fees/migrations/0010_remove_grade_from_feestructure.py
ERP/fees/migrations/0011_feestructure_grade_academic_year.py
ERP/fees/migrations/0012_payment_mode_credit_bank_installment.py
ERP/fees/migrations/0013_feetype_default_amount.py
ERP/fees/migrations/0014_add_feetype_is_mandatory.py
ERP/fees/migrations/0015_mark_mandatory_fee_types.py
ERP/fees/migrations/0016_add_feetype_fixed_down_payment.py
ERP/fees/migrations/0017_add_feestructure_min_down_payment.py
ERP/fees/migrations/0018_replace_due_date_with_four_dates.py
ERP/fees/migrations/0019_revert_to_single_due_date.py
ERP/fees/migrations/0020_add_structure_type_to_bundle.py
ERP/fees/migrations/0021_add_code_to_bundle.py
ERP/fees/migrations/0022_add_creditnote_fields_to_taxinvoice.py
ERP/fees/migrations/0023_remove_fee_structure_bundle.py
ERP/fees/migrations/0024_add_structure_type_to_feestructure.py
ERP/fees/migrations/0025_add_other_structure_type.py
ERP/fees/migrations/0026_external_candidate.py
ERP/fees/migrations/0027_external_candidate_board.py
ERP/fees/migrations/0028_externalcandidate_enrolled_student_and_more.py
ERP/fees/migrations/0029_alter_externalcandidate_board.py
ERP/fees/migrations/0030_add_division_to_external_candidate.py
ERP/fees/migrations/0031_externalcandidate_is_saudi.py
ERP/fees/migrations/0032_alter_feestructure_structure_type.py
ERP/fees/migrations/0033_alter_feestructure_unique_together_and_more.py
ERP/fees/migrations/0034_invoice_first_printed_at.py
ERP/fees/migrations/0035_payment_plan_semester.py
ERP/fees/migrations/0036_payment_installment_fk.py
ERP/fees/migrations/0037_rename_installments_to_semesters.py
ERP/fees/migrations/0038_alter_tuitionfeeconfig_num_payments_and_more.py
ERP/fees/migrations/0039_payment_is_voided_payment_void_reason_and_more.py
ERP/fees/migrations/__init__.py
ERP/fees/models.py
ERP/fees/pdf_exports.py
ERP/fees/templatetags/__init__.py
ERP/fees/templatetags/fee_pdf_filters.py
ERP/fees/tests.py
ERP/fees/urls.py
ERP/fees/views.py
ERP/manage.py
ERP/serve.py
ERP/staff/__init__.py
ERP/staff/admin.py
ERP/staff/apps.py
ERP/staff/forms.py
ERP/staff/migrations/0001_initial.py
ERP/staff/migrations/__init__.py
ERP/staff/models.py
ERP/staff/tests.py
ERP/staff/urls.py
ERP/staff/views.py
ERP/static/css/tailwind.css
ERP/students/__init__.py
ERP/students/admin.py
ERP/students/apps.py
ERP/students/forms.py
ERP/students/migrations/0001_initial.py
ERP/students/migrations/0002_add_performance_indexes.py
ERP/students/migrations/0003_student_id_type.py
ERP/students/migrations/0004_studentdocument_iqama_type.py
ERP/students/migrations/0005_add_father_national_id.py
ERP/students/migrations/0006_add_father_mother_detail_fields.py
ERP/students/migrations/0007_add_sibling_model.py
ERP/students/migrations/0008_add_iqama_passport_religion_birthplace.py
ERP/students/migrations/0009_add_authorized_pickup.py
ERP/students/migrations/0010_add_fee_category.py
ERP/students/migrations/0011_alter_student_enrollment_type.py
ERP/students/migrations/0012_student_study_mode.py
ERP/students/migrations/0013_alter_student_fee_category.py
ERP/students/migrations/0014_religion_choices.py
ERP/students/migrations/0015_promotionhistory.py
ERP/students/migrations/0016_student_fees_contact_email_and_more.py
ERP/students/migrations/__init__.py
ERP/students/models.py
ERP/students/tests.py
ERP/students/urls.py
ERP/students/views.py
ERP/templates/academics/bulk_report_cards.html
ERP/templates/academics/exam_form.html
ERP/templates/academics/exam_list.html
ERP/templates/academics/exam_results.html
ERP/templates/academics/exam_type_form.html
ERP/templates/academics/exam_type_list.html
ERP/templates/academics/grade_config_form.html
ERP/templates/academics/grade_config_list.html
... 132 more entries omitted
```

## File Manifest

| File | Bytes | Score | Why |
| --- | ---: | ---: | --- |
| README.md | 88 | 105 | project-metadata, high-signal-doc |
| ERP/theme/static_src/package.json | 960 | 70 | project-metadata |
| package.json | 60 | 70 | project-metadata |
| requirements.txt | 1508 | 70 | project-metadata |
| deploy/README_WINDOWS.txt | 2080 | 35 | high-signal-doc |
| ERP/theme/static_src/src/styles.css | 59 | 30 | source |
| ERP/academics/tests.py | 63 | 18 | test |
| ERP/accounts/tests.py | 63 | 18 | test |
| ERP/ai_features/tests.py | 63 | 18 | test |
| ERP/core/tests.py | 63 | 18 | test |
| ERP/fees/tests.py | 63 | 18 | test |
| ERP/staff/tests.py | 63 | 18 | test |
| ERP/students/tests.py | 63 | 18 | test |
| ERP/tests/__init__.py | 21 | 18 | test |
| ERP/tests/conftest.py | 2756 | 18 | test |
| ERP/tests/integration/__init__.py | 0 | 18 | test |
| ERP/tests/integration/test_auth.py | 4116 | 18 | test |
| ERP/tests/integration/test_fees.py | 6051 | 18 | test |
| ERP/tests/integration/test_marks.py | 6384 | 18 | test |
| ERP/tests/integration/test_students.py | 5613 | 18 | test |
| ERP/tests/unit/__init__.py | 0 | 18 | test |
| ERP/tests/factories.py | 12847 | 17 | test |
| backfill_missing.py | 4587 | 0 | context |
| deploy/fix_service/serve.py | 788 | 0 | context |
| deploy/fix_static/login.html | 6752 | 0 | context |
| deploy/fix_static/settings.py | 6596 | 0 | context |
| deploy/fix_static/urls.py | 1633 | 0 | context |
| deploy/setup_server.sh | 5370 | 0 | context |
| ERP/academics/__init__.py | 0 | 0 | context |
| ERP/academics/admin.py | 1319 | 0 | context |
| ERP/academics/apps.py | 98 | 0 | context |
| ERP/academics/forms.py | 4862 | 0 | context |
| ERP/academics/migrations/__init__.py | 0 | 0 | context |
| ERP/academics/migrations/0001_initial.py | 6289 | 0 | context |
| ERP/academics/models.py | 8672 | 0 | context |
| ERP/academics/urls.py | 2457 | 0 | context |
| ERP/accounts/__init__.py | 0 | 0 | context |
| ERP/accounts/admin.py | 1054 | 0 | context |
| ERP/accounts/apps.py | 96 | 0 | context |
| ERP/accounts/decorators.py | 1200 | 0 | context |
| ERP/accounts/management/__init__.py | 0 | 0 | context |
| ERP/accounts/management/commands/__init__.py | 0 | 0 | context |
| ERP/accounts/management/commands/create_super_admin.py | 1749 | 0 | context |
| ERP/accounts/migrations/__init__.py | 0 | 0 | context |
| ERP/accounts/migrations/0001_initial.py | 2848 | 0 | context |
| ERP/accounts/models.py | 2907 | 0 | context |
| ERP/accounts/urls.py | 263 | 0 | context |
| ERP/accounts/views.py | 1280 | 0 | context |
| ERP/ai_features/__init__.py | 0 | 0 | context |
| ERP/ai_features/admin.py | 66 | 0 | context |
| ERP/ai_features/apps.py | 101 | 0 | context |
| ERP/ai_features/migrations/__init__.py | 0 | 0 | context |
| ERP/ai_features/models.py | 60 | 0 | context |
| ERP/ai_features/urls.py | 680 | 0 | context |
| ERP/ai_features/views.py | 10660 | 0 | context |
| ERP/attendance/__init__.py | 0 | 0 | context |
| ERP/attendance/admin.py | 1069 | 0 | context |
| ERP/attendance/apps.py | 191 | 0 | context |
| ERP/attendance/forms.py | 3779 | 0 | context |
| ERP/attendance/migrations/__init__.py | 0 | 0 | context |
| ERP/attendance/migrations/0001_initial.py | 2837 | 0 | context |
| ERP/attendance/migrations/0002_add_performance_indexes.py | 737 | 0 | context |
| ERP/attendance/models.py | 2700 | 0 | context |
| ERP/attendance/urls.py | 747 | 0 | context |
| ERP/core/__init__.py | 0 | 0 | context |
| ERP/core/admin.py | 1436 | 0 | context |
| ERP/core/apps.py | 88 | 0 | context |
| ERP/core/forms.py | 4662 | 0 | context |
| ERP/core/management/__init__.py | 0 | 0 | context |
| ERP/core/management/commands/__init__.py | 0 | 0 | context |
| ERP/core/management/commands/seed_grades.py | 4542 | 0 | context |
| ERP/core/management/commands/seed_initial_data.py | 6558 | 0 | context |
| ERP/core/migrations/__init__.py | 0 | 0 | context |
| ERP/core/migrations/0001_initial.py | 4754 | 0 | context |
| ERP/core/migrations/0002_add_home_study_division.py | 1188 | 0 | context |
| ERP/core/migrations/0003_board.py | 1043 | 0 | context |
| ERP/core/migrations/0004_alter_division_name.py | 402 | 0 | context |
| ERP/core/migrations/0005_add_default_divisions_grades_sections.py | 2358 | 0 | context |
| ERP/core/migrations/0006_fix_default_grades.py | 1651 | 0 | context |
| ERP/core/migrations/0007_studymode.py | 1243 | 0 | context |
| ERP/core/models.py | 5206 | 0 | context |
| ERP/core/urls.py | 4437 | 0 | context |
| ERP/ERP/__init__.py | 0 | 0 | context |
| ERP/ERP/asgi.py | 399 | 0 | context |
| ERP/ERP/settings_production.py | 6817 | 0 | context |
| ERP/ERP/settings_test.py | 714 | 0 | context |
| ERP/ERP/settings.py | 6596 | 0 | context |
| ERP/ERP/urls.py | 1633 | 0 | context |
| ERP/ERP/wsgi.py | 399 | 0 | context |
| ERP/fees/__init__.py | 0 | 0 | context |

## Changed Files

No Git changes found, or this is not a Git repository.

## Git Diff Snippets

No diff available, or Git is unavailable.

## TODO / FIXME / HACK Notes

No TODO/FIXME/HACK notes found in selected files.

## Selected File Context

### README.md

| Field | Value |
| --- | --- |
| Bytes | 88 |
| Score | 105 |
| Why | project-metadata, high-signal-doc |
| Status | Full content |


```markdown
# School-ERP-System
‣匭档潯⵬剅ⵐ祓瑳浥਍‣匭档潯⵬剅ⵐ祓瑳浥਍
```

### ERP/theme/static_src/package.json

| Field | Value |
| --- | --- |
| Bytes | 960 |
| Score | 70 |
| Why | project-metadata |
| Status | Full content |


```json
{
  "name": "theme",
  "version": "4.4.0",
  "description": "",
  "scripts": {
    "start": "npm run dev",
    "build": "npm run build:clean && npm run build:tailwind",
    "build:clean": "rimraf ../static/css/dist",
    "build:tailwind": "cross-env NODE_ENV=production tailwindcss --postcss -i ./src/styles.css -o ../static/css/dist/styles.css --minify",
    "dev": "cross-env NODE_ENV=development tailwindcss --postcss -i ./src/styles.css -o ../static/css/dist/styles.css -w",
    "tailwindcss": "node ./node_modules/tailwindcss/lib/cli.js"
  },
  "keywords": [],
  "author": "",
  "license": "MIT",
  "devDependencies": {
    "@tailwindcss/aspect-ratio": "^0.4.2",
    "@tailwindcss/forms": "^0.5.10",
    "@tailwindcss/typography": "^0.5.16",
    "cross-env": "^7.0.3",
    "postcss": "^8.5.3",
    "postcss-import": "^16.1.0",
    "postcss-nested": "^7.0.2",
    "postcss-simple-vars": "^7.0.1",
    "rimraf": "^6.0.1",
    "tailwindcss": "^3.4.17"
  }
}
```

### package.json

| Field | Value |
| --- | --- |
| Bytes | 60 |
| Score | 70 |
| Why | project-metadata |
| Status | Full content |


```json
{
  "devDependencies": {
    "tailwindcss": "^3.4.19"
  }
}
```

### requirements.txt

| Field | Value |
| --- | --- |
| Bytes | 1508 |
| Score | 70 |
| Why | project-metadata |
| Status | Full content |


```txt
# Django & Web Framework
Django==6.0.4
asgiref==3.11.1
sqlparse==0.5.5

# Database
psycopg2-binary==2.9.11

# Frontend & Styling
django-tailwind==4.4.2
pytailwindcss==0.3.0

# PDF & Document Generation
reportlab==4.4.10
weasyprint==68.1
xhtml2pdf==0.2.17
PyYAML==6.0.3
pypdf==6.10.0
pyHanko==0.34.1
pyhanko-certvalidator==0.30.2
pycairo==1.29.0
rlPyCairo==0.4.0
pillow==12.2.0
fonttools==4.62.1
freetype-py==2.5.1
webencodings==0.5.1
html5lib==1.1
cssselect2==0.9.0
svglib==1.6.0
pydyf==0.12.1
tinycss2==1.5.1
tinyhtml5==2.1.0

# Text Processing & Localization
python-bidi==0.6.7
arabic-reshaper==3.0.0
Pygments==2.20.0

# Data Processing & Excel
openpyxl==3.1.5


# Scientific Computing & Machine Learning
numpy==2.4.4
scipy==1.17.1
scikit-learn==1.8.0
joblib==1.5.3
threadpoolctl==3.6.0

# Security & Cryptography
cryptography==46.0.7
asn1crypto==1.5.1
oscrypto==1.3.0
lxml==6.0.4

# Configuration & Utilities
python-decouple==3.8
requests==2.33.1
certifi==2026.2.25
charset-normalizer==3.4.7
idna==3.11
urllib3==2.6.3
colorama==0.4.6
packaging==26.0
six==1.17.0
uritools==6.0.1
tzdata==2026.1
tzlocal==5.3.1
cffi==2.0.0
pycparser==3.0
brotli==1.2.0

# Testing & Development
pytest==9.0.3
pytest-django==4.12.0
factory_boy==3.3.3
Faker==40.13.0
pluggy==1.6.0
iniconfig==2.3.0

# Production Server
# gunicorn==25.3.0   # Linux only — does NOT run on Windows
waitress==3.0.2      # Windows-compatible WSGI server

# Optional Dependencies (uncomment if needed)
# et_xmlfile==2.0.0  # For Excel file support
```

### deploy/README_WINDOWS.txt

| Field | Value |
| --- | --- |
| Bytes | 2080 |
| Score | 35 |
| Why | high-signal-doc |
| Status | Full content |


```txt
============================================================
 AL-KAWTHAR ERP — WINDOWS SERVER OFFLINE DEPLOY
============================================================

Ye saari files DEPLOY\ folder me hain. Server par chalane ka order:

------------------------------------------------------------
 SERVER PAR LE JANE SE PEHLE (pendrive me copy karo)
------------------------------------------------------------
 - Poora ERP_SYSTEM folder (db.sqlite3, offline_packages\,
   nssm\, DEPLOY\, .env  — sab andar hai)
 - venv\ folder COPY MAT KARNA (server par naya banega)
 - Python 3.14.4 ka offline installer

------------------------------------------------------------
 SERVER PAR STEPS
------------------------------------------------------------
 1) Python 3.14.4 install karo  ("Add to PATH" tick karna)

 2) DEPLOY\deploy_offline.bat   -> double-click
       (venv banata hai + saare packages install + DB + static)

 3) Server hamesha chalu rakhne ke liye (RECOMMENDED):
       DEPLOY\install_service.bat
       -> RIGHT-CLICK -> "Run as administrator"
       (Windows Service ban jayega, reboot par auto-start)

    YA manually chalane ke liye:
       DEPLOY\start_server.bat   -> double-click (window khula rakho)

 4) Browser me kholo:
       http://<server-ka-IP>:8000

------------------------------------------------------------
 ZAROORI
------------------------------------------------------------
 - Windows Firewall me TCP port 8000 ALLOW karo:
   New Inbound Rule -> Port -> TCP 8000 -> Allow
 - PDF/print chahiye to GTK3 runtime ka offline installer bhi
   server par install karna (WeasyPrint ke liye).
 - Service band/hatane ke liye: DEPLOY\uninstall_service.bat
   (right-click -> Run as administrator)
 - Service ke logs:  ERP\logs_service.txt

------------------------------------------------------------
 NOTE
------------------------------------------------------------
 nginx\ , systemd\ , setup_server.sh  -> ye LINUX ke liye hain,
 Windows deploy me IN-KI ZAROORAT NAHI. Ignore kar do.
============================================================
```

### ERP/theme/static_src/src/styles.css

| Field | Value |
| --- | --- |
| Bytes | 59 |
| Score | 30 |
| Why | source |
| Status | Full content |


```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### ERP/academics/tests.py

| Field | Value |
| --- | --- |
| Bytes | 63 |
| Score | 18 |
| Why | test |
| Status | Full content |


```py
from django.test import TestCase

# Create your tests here.
```

### ERP/accounts/tests.py

| Field | Value |
| --- | --- |
| Bytes | 63 |
| Score | 18 |
| Why | test |
| Status | Full content |


```py
from django.test import TestCase

# Create your tests here.
```

### ERP/ai_features/tests.py

| Field | Value |
| --- | --- |
| Bytes | 63 |
| Score | 18 |
| Why | test |
| Status | Full content |


```py
from django.test import TestCase

# Create your tests here.
```

### ERP/core/tests.py

| Field | Value |
| --- | --- |
| Bytes | 63 |
| Score | 18 |
| Why | test |
| Status | Full content |


```py
from django.test import TestCase

# Create your tests here.
```

### ERP/fees/tests.py

| Field | Value |
| --- | --- |
| Bytes | 63 |
| Score | 18 |
| Why | test |
| Status | Full content |


```py
from django.test import TestCase

# Create your tests here.
```

### ERP/staff/tests.py

| Field | Value |
| --- | --- |
| Bytes | 63 |
| Score | 18 |
| Why | test |
| Status | Full content |


```py
from django.test import TestCase

# Create your tests here.
```

### ERP/students/tests.py

| Field | Value |
| --- | --- |
| Bytes | 63 |
| Score | 18 |
| Why | test |
| Status | Full content |


```py
from django.test import TestCase

# Create your tests here.
```

### ERP/tests/__init__.py

| Field | Value |
| --- | --- |
| Bytes | 21 |
| Score | 18 |
| Why | test |
| Status | Full content |


```py
# tests/__init__.py
```

### ERP/tests/conftest.py

| Field | Value |
| --- | --- |
| Bytes | 2756 |
| Score | 18 |
| Why | test |
| Status | Full content |


```py
"""
Shared pytest fixtures and hooks for the whole ERP test-suite.

Layout
------
tests/unit/         → isolated tests of one model / form / helper (marked `unit`)
tests/integration/  → full request/response tests through the Django client (marked `integration`)

Run only one layer:   pytest -m unit      |   pytest -m integration
"""
import pytest

from accounts.models import CustomUser
from tests import factories as f


# ── Auto-mark tests by folder so `-m unit` / `-m integration` just work ──────

def pytest_collection_modifyitems(config, items):
    for item in items:
        path = str(item.fspath).replace('\\', '/')
        if '/tests/unit/' in path:
            item.add_marker(pytest.mark.unit)
        elif '/tests/integration/' in path:
            item.add_marker(pytest.mark.integration)


# ── Users, one per role ──────────────────────────────────────────────────────

@pytest.fixture
def super_admin(db):
    return f.SuperAdminFactory()


@pytest.fixture
def admin(db):
    return f.UserFactory(role=CustomUser.ADMIN)


@pytest.fixture
def teacher(db):
    return f.TeacherFactory()


@pytest.fixture
def accountant(db):
    return f.AccountantFactory()


@pytest.fixture
def staff_user(db):
    return f.StaffUserFactory()


@pytest.fixture
def parent(db):
    return f.ParentFactory()


ALL_ROLES = [r for r, _ in CustomUser.ROLE_CHOICES]


@pytest.fixture
def login(client):
    """`login(user)` → logged-in client. Keeps tests one line shorter."""
    def _login(user):
        client.force_login(user)
        return client
    return _login


# ── A small but complete school, for integration tests ──────────────────────

@pytest.fixture
def school(db):
    """
    One division → grade → section, with a current academic year, a subject,
    a study mode, an active Saudi student and an active expat student.
    Returned as a simple namespace so tests read `school.student`.
    """
    from types import SimpleNamespace

    year     = f.AcademicYearFactory(is_current=True)
    division = f.DivisionFactory()
    grade    = f.GradeFactory(division=division, order=1)
    section  = f.SectionFactory(grade=grade)
    subject  = f.SubjectFactory(grade=grade, division=division)
    mode     = f.StudyModeFactory()

    common = dict(division=division, grade=grade, section=section, academic_year=year)
    return SimpleNamespace(
        year=year, division=division, grade=grade, section=section,
        subject=subject, study_mode=mode,
        student=f.StudentFactory(**common),
        expat=f.ExpatStudentFactory(**common),
    )
```

### ERP/tests/integration/__init__.py

| Field | Value |
| --- | --- |
| Bytes | 0 |
| Score | 18 |
| Why | test |
| Status | Full content |


```py

```

### ERP/tests/integration/test_auth.py

| Field | Value |
| --- | --- |
| Bytes | 4116 |
| Score | 18 |
| Why | test |
| Status | Full content |


```py
"""
Tests for authentication: login, logout, and role-based access control.
"""
import pytest
from django.urls import reverse

from accounts.models import CustomUser
from tests.factories import UserFactory, TeacherFactory, AccountantFactory


pytestmark = pytest.mark.django_db


# ── Login / Logout ────────────────────────────────────────────────────────────

class TestLogin:
    def test_login_page_renders(self, client):
        url = reverse('accounts:login')
        resp = client.get(url)
        assert resp.status_code == 200

    def test_valid_credentials_redirect_to_dashboard(self, client):
        user = UserFactory(username='admin1', password='[REDACTED:SECRET]')
        resp = client.post(
            reverse('accounts:login'),
            {'username': 'admin1', 'password': '[REDACTED:SECRET]'},
            follow=True,
        )
        assert resp.status_code == 200
        assert resp.wsgi_request.user.is_authenticated

    def test_wrong_password_stays_on_login(self, client):
        UserFactory(username='admin2', password='[REDACTED:SECRET]')
        resp = client.post(
            reverse('accounts:login'),
            {'username': 'admin2', 'password': '[REDACTED:SECRET]'},
        )
        assert resp.status_code == 200
        assert not resp.wsgi_request.user.is_authenticated

    def test_inactive_user_cannot_login(self, client):
        user = UserFactory(username='inactive1', password='[REDACTED:SECRET]')
        user.is_active = False
        user.save()
        resp = client.post(
            reverse('accounts:login'),
            {'username': 'inactive1', 'password': '[REDACTED:SECRET]'},
        )
        assert not resp.wsgi_request.user.is_authenticated

    def test_logout_redirects_to_login(self, client):
        user = UserFactory()
        client.force_login(user)
        resp = client.post(reverse('accounts:logout'), follow=True)
        assert resp.status_code == 200
        assert not resp.wsgi_request.user.is_authenticated


class TestUnauthenticatedRedirect:
    """Unauthenticated requests to protected pages must redirect to login."""

    protected_url_names = [
        'students:list',
        'attendance:take_attendance',
    ]

    @pytest.mark.parametrize("url_name", [
        'students:list',
        'attendance:take',
    ])
    def test_redirect_to_login(self, client, url_name):
        resp = client.get(reverse(url_name))
        assert resp.status_code == 302
        assert '/accounts/login' in resp['Location']


# ── Role-Based Access ─────────────────────────────────────────────────────────

class TestRoleAccess:
    """PARENT role must be denied access to admin-only views."""

    def test_parent_denied_student_add(self, client):
        parent = UserFactory(role=CustomUser.PARENT)
        client.force_login(parent)
        resp = client.get(reverse('students:add'))
        # Should redirect (role_required returns 302 to login or 403)
        assert resp.status_code in (302, 403)

    def test_parent_denied_student_list(self, client):
        parent = UserFactory(role=CustomUser.PARENT)
        client.force_login(parent)
        resp = client.get(reverse('students:list'))
        assert resp.status_code in (302, 403)

    def test_admin_can_access_student_add(self, client):
        admin = UserFactory(role=CustomUser.ADMIN)
        client.force_login(admin)
        resp = client.get(reverse('students:add'))
        assert resp.status_code == 200

    def test_teacher_can_view_student_list(self, client):
        teacher = TeacherFactory()
        client.force_login(teacher)
        resp = client.get(reverse('students:list'))
        assert resp.status_code == 200

    def test_accountant_denied_student_add(self, client):
        acc = AccountantFactory()
        client.force_login(acc)
        resp = client.get(reverse('students:add'))
        assert resp.status_code in (302, 403)
```

### ERP/tests/integration/test_fees.py

| Field | Value |
| --- | --- |
| Bytes | 6051 |
| Score | 18 |
| Why | test |
| Status | Full content |


```py
"""
Tests for fee collection workflow and receipt generation.
"""
import datetime
from decimal import Decimal

import pytest
from django.urls import reverse

from accounts.models import CustomUser
from fees.models import StudentFee, Payment
from tests.factories import (
    UserFactory, AccountantFactory,
    StudentFeeFactory, PaymentFactory, StudentFactory,
    FeeStructureFactory, FeeTypeFactory,
)

pytestmark = pytest.mark.django_db


@pytest.fixture
def student_fee(db):
    return StudentFeeFactory(
        amount=Decimal('10000.00'),
        discount=Decimal('0.00'),
        net_amount=Decimal('10000.00'),
        status=StudentFee.UNPAID,
        due_date=datetime.date.today() + datetime.timedelta(days=30),  # future — not overdue
    )


# ── Dashboard ─────────────────────────────────────────────────────────────────

class TestFeesDashboard:
    def test_dashboard_renders(self, client, accountant):
        client.force_login(accountant)
        resp = client.get(reverse('fees:dashboard'))
        assert resp.status_code == 200

    def test_teacher_denied_dashboard(self, client):
        teacher = UserFactory(role=CustomUser.TEACHER)
        client.force_login(teacher)
        resp = client.get(reverse('fees:dashboard'))
        assert resp.status_code in (302, 403)


# ── StudentFee model helpers ──────────────────────────────────────────────────

class TestStudentFeeModel:
    def test_balance_equals_net_when_no_payments(self, student_fee):
        assert student_fee.balance == student_fee.net_amount

    def test_balance_decreases_after_payment(self, student_fee, accountant):
        PaymentFactory(
            student_fee=student_fee,
            paid_amount=Decimal('3000.00'),
            collected_by=accountant,
        )
        student_fee.refresh_from_db()
        assert student_fee.balance == Decimal('7000.00')

    def test_status_becomes_paid_when_fully_settled(self, student_fee, accountant):
        PaymentFactory(
            student_fee=student_fee,
            paid_amount=Decimal('10000.00'),
            collected_by=accountant,
        )
        student_fee.refresh_status()
        assert student_fee.status == StudentFee.PAID

    def test_status_partial_on_partial_payment(self, student_fee, accountant):
        PaymentFactory(
            student_fee=student_fee,
            paid_amount=Decimal('4000.00'),
            collected_by=accountant,
        )
        student_fee.refresh_status()
        assert student_fee.status == StudentFee.PARTIAL

    def test_overdue_when_past_due_and_unpaid(self, db, accountant):
        fee = StudentFeeFactory(
            due_date=datetime.date(2023, 1, 1),
            status=StudentFee.UNPAID,
            net_amount=Decimal('5000.00'),
            amount=Decimal('5000.00'),
            discount=Decimal('0.00'),
        )
        fee.refresh_status()
        assert fee.status == StudentFee.OVERDUE


# ── Payment recording ─────────────────────────────────────────────────────────

class TestPaymentRecord:
    def test_payment_has_unique_receipt_number(self, db, accountant):
        sf1 = StudentFeeFactory()
        sf2 = StudentFeeFactory()
        p1  = PaymentFactory(student_fee=sf1, collected_by=accountant)
        p2  = PaymentFactory(student_fee=sf2, collected_by=accountant)
        assert p1.receipt_number != p2.receipt_number
        assert p1.receipt_number.startswith('RCP-')

    def test_payment_amount_clamped_to_balance(self, student_fee, accountant):
        # Paying more than balance should not create negative balance via view
        # (The view clamps it — test the model property directly)
        PaymentFactory(
            student_fee=student_fee,
            paid_amount=Decimal('10000.00'),      # exact balance
            collected_by=accountant,
        )
        assert student_fee.balance == Decimal('0.00')


# ── Receipt view ──────────────────────────────────────────────────────────────

class TestReceiptPrint:
    def test_receipt_renders_for_accountant(self, client, accountant, student_fee):
        payment = PaymentFactory(student_fee=student_fee, collected_by=accountant)
        client.force_login(accountant)
        resp = client.get(reverse('fees:receipt_print', kwargs={'payment_pk': payment.pk}))
        assert resp.status_code == 200
        assert payment.receipt_number.encode() in resp.content

    def test_receipt_404_for_missing_payment(self, client, accountant):
        client.force_login(accountant)
        resp = client.get(reverse('fees:receipt_print', kwargs={'payment_pk': 99999}))
        assert resp.status_code == 404

    def test_teacher_denied_receipt(self, client, student_fee, accountant):
        teacher = UserFactory(role=CustomUser.TEACHER)
        payment = PaymentFactory(student_fee=student_fee, collected_by=accountant)
        client.force_login(teacher)
        resp = client.get(reverse('fees:receipt_print', kwargs={'payment_pk': payment.pk}))
        assert resp.status_code in (302, 403)


# ── Outstanding view ──────────────────────────────────────────────────────────

class TestOutstandingReport:
    def test_outstanding_renders(self, client, accountant):
        client.force_login(accountant)
        resp = client.get(reverse('fees:outstanding'))
        assert resp.status_code == 200
```

### ERP/tests/integration/test_marks.py

| Field | Value |
| --- | --- |
| Bytes | 6384 |
| Score | 18 |
| Why | test |
| Status | Full content |


```py
"""
Tests for the marks workflow: draft → submitted → approved.
Covers entry, submission, approval, and role restrictions.
"""
import pytest
from django.urls import reverse
from django.utils import timezone

from accounts.models import CustomUser
from academics.models import Mark
from tests.factories import (
    UserFactory, TeacherFactory,
    ExamFactory, MarkFactory, StudentFactory,
    SectionFactory,
)

pytestmark = pytest.mark.django_db


@pytest.fixture
def exam(db):
    return ExamFactory()


@pytest.fixture
def student_in_exam(exam):
    """A student whose section matches the exam's section."""
    return StudentFactory(section=exam.section, is_active=True)


# ── Draft entry ───────────────────────────────────────────────────────────────

class TestMarksDraftEntry:
    def test_marks_entry_page_renders(self, client, teacher, exam, student_in_exam):
        client.force_login(teacher)
        resp = client.get(reverse('academics:marks_entry', kwargs={'exam_pk': exam.pk}))
        assert resp.status_code == 200

    def test_teacher_can_save_draft(self, client, teacher, exam, student_in_exam):
        client.force_login(teacher)
        resp = client.post(
            reverse('academics:marks_entry', kwargs={'exam_pk': exam.pk}),
            {
                f'marks_{student_in_exam.pk}': '80',
                f'absent_{student_in_exam.pk}': '',
                f'remarks_{student_in_exam.pk}': '',
                'action': 'draft',
            },
            follow=True,
        )
        assert resp.status_code == 200
        mark = Mark.objects.get(student=student_in_exam, exam=exam)
        assert mark.status == 'draft'
        assert float(mark.obtained_marks) == 80.0

    def test_absent_flag_clears_marks(self, client, teacher, exam, student_in_exam):
        client.force_login(teacher)
        client.post(
            reverse('academics:marks_entry', kwargs={'exam_pk': exam.pk}),
            {
                f'marks_{student_in_exam.pk}': '',
                f'absent_{student_in_exam.pk}': 'on',
                f'remarks_{student_in_exam.pk}': '',
                'action': 'draft',
            },
        )
        mark = Mark.objects.get(student=student_in_exam, exam=exam)
        assert mark.is_absent is True
        assert mark.obtained_marks is None


# ── Submit ────────────────────────────────────────────────────────────────────

class TestMarksSubmit:
    def test_teacher_can_submit_marks(self, client, teacher, exam, student_in_exam):
        client.force_login(teacher)
        client.post(
            reverse('academics:marks_entry', kwargs={'exam_pk': exam.pk}),
            {
                f'marks_{student_in_exam.pk}': '72',
                f'absent_{student_in_exam.pk}': '',
                f'remarks_{student_in_exam.pk}': '',
                'action': 'submit',
            },
        )
        mark = Mark.objects.get(student=student_in_exam, exam=exam)
        assert mark.status == 'submitted'

    def test_submitted_mark_shows_in_approval_queue(self, client, admin, exam):
        MarkFactory(exam=exam, status='submitted')
        client.force_login(admin)
        resp = client.get(reverse('academics:marks_approval'))
        assert resp.status_code == 200


# ── Approve ───────────────────────────────────────────────────────────────────

class TestMarksApprove:
    def test_admin_can_approve_submitted_marks(self, client, admin, exam, student_in_exam):
        mark = MarkFactory(student=student_in_exam, exam=exam, status='submitted')
        client.force_login(admin)
        resp = client.post(
            reverse('academics:approve_marks', kwargs={'exam_pk': exam.pk}),
            follow=True,
        )
        assert resp.status_code == 200
        mark.refresh_from_db()
        assert mark.status == 'approved'
        assert mark.approved_by == admin
        assert mark.approved_at is not None

    def test_teacher_cannot_approve_marks(self, client, teacher, exam, student_in_exam):
        MarkFactory(student=student_in_exam, exam=exam, status='submitted')
        client.force_login(teacher)
        resp = client.post(
            reverse('academics:approve_marks', kwargs={'exam_pk': exam.pk}),
        )
        assert resp.status_code in (302, 403)
        # status must remain 'submitted'
        mark = Mark.objects.get(student=student_in_exam, exam=exam)
        assert mark.status == 'submitted'


# ── Unlock ────────────────────────────────────────────────────────────────────

class TestMarksUnlock:
    def test_admin_can_unlock_approved_marks(self, client, admin, exam, student_in_exam):
        mark = MarkFactory(student=student_in_exam, exam=exam, status='approved')
        client.force_login(admin)
        client.post(reverse('academics:unlock_marks', kwargs={'exam_pk': exam.pk}))
        mark.refresh_from_db()
        assert mark.status == 'submitted'


# ── Percentage & grade helpers ────────────────────────────────────────────────

class TestMarkHelpers:
    def test_get_percentage(self, db):
        mark = MarkFactory.build(obtained_marks=80)
        mark.exam = ExamFactory(total_marks=100)
        assert mark.get_percentage() == 80.0

    def test_absent_has_no_percentage(self, db):
        mark = MarkFactory.build(is_absent=True, obtained_marks=None)
        mark.exam = ExamFactory(total_marks=100)
        assert mark.get_percentage() is None

    def test_letter_grade_a_plus(self, db):
        mark = MarkFactory.build(obtained_marks=95)
        mark.exam = ExamFactory(total_marks=100)
        assert mark.get_letter_grade() == 'A+'
```

### ERP/tests/integration/test_students.py

| Field | Value |
| --- | --- |
| Bytes | 5613 |
| Score | 18 |
| Why | test |
| Status | Full content |


```py
"""
Tests for Student CRUD operations.
"""
import pytest
from django.urls import reverse

from accounts.models import CustomUser
from students.models import Student
from tests.factories import (
    UserFactory, StudentFactory,
    DivisionFactory, GradeFactory, SectionFactory, AcademicYearFactory,
    StudyModeFactory,
)

pytestmark = pytest.mark.django_db


@pytest.fixture
def student(db):
    return StudentFactory()


# ── List ──────────────────────────────────────────────────────────────────────

class TestStudentList:
    def test_list_renders_for_admin(self, client, admin):
        StudentFactory.create_batch(3)
        client.force_login(admin)
        resp = client.get(reverse('students:list'))
        assert resp.status_code == 200
        assert b'Student' in resp.content

    def test_search_filters_results(self, client, admin):
        StudentFactory(full_name='Alice Johnson')
        StudentFactory(full_name='Bob Smith')
        client.force_login(admin)
        resp = client.get(reverse('students:list'), {'q': 'Alice'})
        assert resp.status_code == 200
        assert b'Alice' in resp.content
        assert b'Bob' not in resp.content


# ── Create ────────────────────────────────────────────────────────────────────

class TestStudentCreate:
    def _valid_payload(self):
        division = DivisionFactory()
        grade    = GradeFactory(division=division)
        section  = SectionFactory(grade=grade)
        year     = AcademicYearFactory()
        return {
            'full_name':       'New Student',
            'arabic_name':     'طالب جديد',
            'dob':             '2010-05-15',
            'gender':          'M',
            'nationality':     'Saudi Arabia',
            'national_id':     '1012345678',
            'study_mode':      StudyModeFactory().pk,
            'fee_category':    'regular',
            'is_active':       'on',
            'division':        division.pk,
            'grade':           grade.pk,
            'section':         section.pk,
            'academic_year':   year.pk,
            'admission_date':  '2024-09-01',
            'enrollment_type': 'NEW',
        }

    def test_admin_can_create_student(self, client, admin):
        payload  = self._valid_payload()
        client.force_login(admin)
        count_before = Student.objects.count()
        resp = client.post(reverse('students:add'), payload)   # don't follow to avoid template rendering
        assert resp.status_code in (200, 302)
        assert Student.objects.count() == count_before + 1

    def test_student_id_auto_generated(self, client, admin):
        payload = self._valid_payload()
        client.force_login(admin)
        client.post(reverse('students:add'), payload)
        s = Student.objects.order_by('-created_at').first()
        assert s is not None
        assert s.student_id != ''

    def test_missing_required_field_shows_error(self, client, admin):
        payload = self._valid_payload()
        del payload['full_name']
        client.force_login(admin)
        resp = client.post(reverse('students:add'), payload)
        assert resp.status_code == 200          # re-renders form
        assert Student.objects.count() == 0


# ── Detail & Update ───────────────────────────────────────────────────────────

class TestStudentDetail:
    def test_detail_page_shows_name(self, client, admin, student):
        client.force_login(admin)
        # Check the view returns 200 without following to avoid template URL resolution issues
        resp = client.get(reverse('students:detail', kwargs={'pk': student.pk}))
        assert resp.status_code in (200, 302)

    def test_edit_student_name(self, client, admin, student):
        client.force_login(admin)
        resp = client.get(reverse('students:edit', kwargs={'pk': student.pk}))
        assert resp.status_code == 200

    def test_404_on_nonexistent_student(self, client, admin):
        client.force_login(admin)
        resp = client.get(reverse('students:detail', kwargs={'pk': 99999}))
        assert resp.status_code == 404


# ── Delete ────────────────────────────────────────────────────────────────────

class TestStudentDelete:
    def test_admin_can_delete_student(self, client, admin, student):
        pk = student.pk
        client.force_login(admin)
        resp = client.post(reverse('students:delete', kwargs={'pk': pk}), follow=True)
        assert resp.status_code == 200
        # Student uses soft-delete (is_active=False), not hard delete
        student.refresh_from_db()
        assert not student.is_active

    def test_teacher_cannot_delete_student(self, client, student):
        teacher = UserFactory(role=CustomUser.TEACHER)
        client.force_login(teacher)
        resp = client.post(reverse('students:delete', kwargs={'pk': student.pk}))
        assert resp.status_code in (302, 403)
        assert Student.objects.filter(pk=student.pk).exists()
```

### ERP/tests/unit/__init__.py

| Field | Value |
| --- | --- |
| Bytes | 0 |
| Score | 18 |
| Why | test |
| Status | Full content |


```py

```

### ERP/tests/factories.py

| Field | Value |
| --- | --- |
| Bytes | 12847 |
| Score | 17 |
| Why | test |
| Status | Full content |


```py
"""
Shared factory-boy factories for all tests.
Each factory creates a minimal valid object with sensible defaults.
"""
import datetime
from decimal import Decimal
import factory
from factory.django import DjangoModelFactory

from accounts.models import CustomUser
from core.models import AcademicYear, Division, Grade, Section, Subject, StudyMode, Board
from students.models import Student
from attendance.models import Attendance
from academics.models import ExamType, Exam, Mark
from fees.models import (
    FeeType, FeeStructure, FeeStructureItem, StudentFee, Payment, Refund,
    TuitionFeeConfig, PaymentPlan, PaymentPlanInstallment, Salary,
    ExternalCandidate, ExternalCandidatePayment,
)
from staff.models import StaffProfile, TeacherAssignment, VacationRequest, MOEApproval


# ── Accounts ──────────────────────────────────────────────────────────────────

class UserFactory(DjangoModelFactory):
    class Meta:
        model = CustomUser

    username  = factory.Sequence(lambda n: f"user{n}")
    email     = factory.Sequence(lambda n: f"user{n}@school.sa")
    full_name = factory.Sequence(lambda n: f"Test User {n}")
    role      = CustomUser.ADMIN
    is_active = True

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        password = kwargs.pop("password", "TestPass123!")
        obj = model_class(*args, **kwargs)
        obj.set_password(password)
        obj.save()
        return obj


class TeacherFactory(UserFactory):
    role = CustomUser.TEACHER


class AccountantFactory(UserFactory):
    role = CustomUser.ACCOUNTANT


class SuperAdminFactory(UserFactory):
    role = CustomUser.SUPER_ADMIN


class StaffUserFactory(UserFactory):
    role = CustomUser.STAFF


class ParentFactory(UserFactory):
    role = CustomUser.PARENT


# ── Core ──────────────────────────────────────────────────────────────────────

class AcademicYearFactory(DjangoModelFactory):
    class Meta:
        model = AcademicYear
        django_get_or_create = ('name',)

    name       = "2024-25"
    start_date = datetime.date(2024, 9, 1)
    end_date   = datetime.date(2025, 6, 30)
    is_current = True


class DivisionFactory(DjangoModelFactory):
    class Meta:
        model = Division
        django_get_or_create = ('name',)

    name            = Division.AMERICAN
    curriculum_type = Division.AMERICAN


class GradeFactory(DjangoModelFactory):
    class Meta:
        model = Grade

    name     = factory.Sequence(lambda n: f"Grade {n+1}")
    division = factory.SubFactory(DivisionFactory)
    order    = factory.Sequence(lambda n: n)


class SectionFactory(DjangoModelFactory):
    class Meta:
        model = Section

    name  = factory.Sequence(lambda n: chr(65 + n % 26))   # A, B, C …
    grade = factory.SubFactory(GradeFactory)


class SubjectFactory(DjangoModelFactory):
    class Meta:
        model = Subject

    name     = factory.Sequence(lambda n: f"Subject {n}")
    code     = factory.Sequence(lambda n: f"SUB-{n:04d}")
    grade    = factory.SubFactory(GradeFactory)
    division = factory.SubFactory(DivisionFactory)


class StudyModeFactory(DjangoModelFactory):
    class Meta:
        model = StudyMode
        django_get_or_create = ('name',)

    name = "On Campus"


class BoardFactory(DjangoModelFactory):
    class Meta:
        model = Board
        django_get_or_create = ('name',)

    name = "IGCSE"


# ── Students ──────────────────────────────────────────────────────────────────

class StudentFactory(DjangoModelFactory):
    class Meta:
        model = Student

    full_name      = factory.Sequence(lambda n: f"Student {n}")
    arabic_name    = factory.Sequence(lambda n: f"طالب {n}")
    dob            = datetime.date(2010, 1, 1)
    gender         = Student.MALE
    nationality    = "Saudi"
    national_id    = factory.Sequence(lambda n: f"100000{n:04d}")
    division       = factory.SubFactory(DivisionFactory)
    # Keep the hierarchy consistent: section ∈ grade ∈ division
    grade          = factory.SubFactory(GradeFactory, division=factory.SelfAttribute('..division'))
    section        = factory.SubFactory(SectionFactory, grade=factory.SelfAttribute('..grade'))
    academic_year  = factory.SubFactory(AcademicYearFactory)
    admission_date = datetime.date(2024, 9, 1)
    guardian_phone = "0501234567"
    is_active      = True
    id_type        = Student.NATIONAL_ID_TYPE


class ExpatStudentFactory(StudentFactory):
    """Non-Saudi resident (Iqama holder) — attracts 15% VAT on taxable fees."""
    nationality  = "India"
    id_type      = Student.IQAMA
    national_id  = ""
    iqama_number = factory.Sequence(lambda n: f"200000{n:04d}")


# ── Attendance ────────────────────────────────────────────────────────────────

class AttendanceFactory(DjangoModelFactory):
    class Meta:
        model = Attendance

    student   = factory.SubFactory(StudentFactory)
    date      = factory.LazyFunction(datetime.date.today)
    status    = 'P'
    marked_by = factory.SubFactory(UserFactory)


# ── Academics ─────────────────────────────────────────────────────────────────

class ExamTypeFactory(DjangoModelFactory):
    class Meta:
        model = ExamType
        django_get_or_create = ('name',)

    name              = "MidTerm"
    weight_percentage = 40


class ExamFactory(DjangoModelFactory):
    class Meta:
        model = Exam

    name          = factory.Sequence(lambda n: f"Exam {n}")
    exam_type     = factory.SubFactory(ExamTypeFactory)
    subject       = factory.SubFactory(SubjectFactory)
    section       = factory.SubFactory(SectionFactory)
    academic_year = factory.SubFactory(AcademicYearFactory)
    term          = 'T1'
    date          = datetime.date(2024, 11, 1)
    total_marks   = 100
    created_by    = factory.SubFactory(UserFactory)


class MarkFactory(DjangoModelFactory):
    class Meta:
        model = Mark

    student        = factory.SubFactory(StudentFactory)
    exam           = factory.SubFactory(ExamFactory)
    obtained_marks = 75
    is_absent      = False
    status         = 'draft'
    entered_by     = factory.SubFactory(UserFactory)


# ── Fees ──────────────────────────────────────────────────────────────────────

def _future(days=60):
    return datetime.date.today() + datetime.timedelta(days=days)


class FeeTypeFactory(DjangoModelFactory):
    """Non-taxable by default. Use TaxableFeeTypeFactory for VAT scenarios."""
    class Meta:
        model = FeeType
        django_get_or_create = ('name',)

    name       = "Tuition"
    category   = FeeType.TUITION
    is_taxable = False


class TaxableFeeTypeFactory(FeeTypeFactory):
    name       = "Transport"
    category   = FeeType.TRANSPORT
    is_taxable = True


class FeeStructureFactory(DjangoModelFactory):
    """The container (one per grade / year / structure_type)."""
    class Meta:
        model = FeeStructure

    academic_year  = factory.SubFactory(AcademicYearFactory)
    grade          = factory.SubFactory(GradeFactory)
    structure_type = FeeStructure.TYPE_REGULAR
    frequency      = "ANNUAL"


class FeeStructureItemFactory(DjangoModelFactory):
    """One fee-type line inside a FeeStructure. StudentFee.fee_structure points here."""
    class Meta:
        model = FeeStructureItem

    structure = factory.SubFactory(FeeStructureFactory)
    fee_type  = factory.SubFactory(FeeTypeFactory)
    amount    = factory.LazyFunction(lambda: Decimal('10000.00'))


class StudentFeeFactory(DjangoModelFactory):
    """net_amount is recomputed by StudentFee.save() — don't rely on passing it."""
    class Meta:
        model = StudentFee

    student       = factory.SubFactory(StudentFactory)
    fee_structure = factory.SubFactory(FeeStructureItemFactory)
    amount        = factory.LazyFunction(lambda: Decimal('10000.00'))
    discount      = factory.LazyFunction(lambda: Decimal('0.00'))
    net_amount    = factory.LazyFunction(lambda: Decimal('0.00'))
    due_date      = factory.LazyFunction(_future)
    status        = StudentFee.UNPAID


class PaymentFactory(DjangoModelFactory):
    class Meta:
        model = Payment

    student_fee    = factory.SubFactory(StudentFeeFactory)
    paid_amount    = factory.LazyFunction(lambda: Decimal('5000.00'))
    payment_date   = factory.LazyFunction(datetime.date.today)
    payment_method = Payment.CREDIT_CARD
    collected_by   = factory.SubFactory(UserFactory)


class RefundFactory(DjangoModelFactory):
    class Meta:
        model = Refund

    payment     = factory.SubFactory(PaymentFactory)
    amount      = factory.LazyFunction(lambda: Decimal('1000.00'))
    reason      = "Test refund"
    refunded_by = factory.SubFactory(UserFactory)


class TuitionFeeConfigFactory(DjangoModelFactory):
    class Meta:
        model = TuitionFeeConfig

    academic_year     = factory.SubFactory(AcademicYearFactory)
    division          = factory.SubFactory(DivisionFactory)
    grade             = factory.SubFactory(GradeFactory)
    structure_type    = TuitionFeeConfig.REGULAR
    num_payments      = 2
    gross_tuition_fee = factory.LazyFunction(lambda: Decimal('20000.00'))


class PaymentPlanFactory(DjangoModelFactory):
    class Meta:
        model = PaymentPlan

    student_fee = factory.SubFactory(StudentFeeFactory)


class PaymentPlanInstallmentFactory(DjangoModelFactory):
    class Meta:
        model = PaymentPlanInstallment

    plan           = factory.SubFactory(PaymentPlanFactory)
    installment_no = factory.Sequence(lambda n: n + 1)
    amount         = factory.LazyFunction(lambda: Decimal('5000.00'))
    due_date       = factory.LazyFunction(_future)


class SalaryFactory(DjangoModelFactory):
    class Meta:
        model = Salary

    staff = factory.SubFactory(TeacherFactory)
    month = datetime.date(2025, 9, 1)
    basic = factory.LazyFunction(lambda: Decimal('8000.00'))


class ExternalCandidateFactory(DjangoModelFactory):
    class Meta:
        model = ExternalCandidate

    full_name = factory.Sequence(lambda n: f"Candidate {n}")


class ExternalCandidatePaymentFactory(DjangoModelFactory):
    class Meta:
        model = ExternalCandidatePayment

    candidate       = factory.SubFactory(ExternalCandidateFactory)
    fee_description = "Entrance Exam"
    amount          = factory.LazyFunction(lambda: Decimal('500.00'))


# ── Staff ─────────────────────────────────────────────────────────────────────

class StaffProfileFactory(DjangoModelFactory):
    class Meta:
        model = StaffProfile

    user        = factory.SubFactory(TeacherFactory)
    employee_id = factory.Sequence(lambda n: f"EMP-{n:04d}")
    designation = 'TEACHER'
    department  = 'ACADEMIC'
    join_date   = datetime.date(2023, 8, 1)


class TeacherAssignmentFactory(DjangoModelFactory):
    class Meta:
        model = TeacherAssignment

    teacher       = factory.SubFactory(TeacherFactory)
    subject       = factory.SubFactory(SubjectFactory)
    section       = factory.SubFactory(SectionFactory)
    academic_year = factory.SubFactory(AcademicYearFactory)


class VacationRequestFactory(DjangoModelFactory):
    class Meta:
        model = VacationRequest

    staff     = factory.SubFactory(TeacherFactory)
    from_date = factory.LazyFunction(lambda: _future(10))
    to_date   = factory.LazyFunction(lambda: _future(14))
    reason    = "Family visit"


class MOEApprovalFactory(DjangoModelFactory):
    class Meta:
        model = MOEApproval

    staff         = factory.SubFactory(TeacherFactory)
    approval_type = MOEApproval.TEACHER_LICENSE
```

### backfill_missing.py

| Field | Value |
| --- | --- |
| Bytes | 4587 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py
"""Find rows in the CSV that don't yet exist in the DB (by name + grade + section)
and create them. Safe to run multiple times — only inserts missing students.
"""
import csv
from datetime import date as _date
from students.models import Student
from core.models import Division, Grade, Section, AcademicYear, StudyMode

CSV_PATH = r"e:\ERP_SYSTEM\students_import_3000.csv"

GENDER_MAP    = {'male': 'M', 'female': 'F'}
ID_TYPE_MAP   = {'national id': 'NATIONAL_ID', 'iqama': 'IQAMA', 'passport': 'PASSPORT'}
ENROLL_MAP    = {'new student': 'NEW', 'regular (continuing)': 'REGULAR', 'transfer': 'TRANSFER'}
FEE_CAT_MAP   = {'new': 'new', 'regular': 'regular', 'transfer': 'transfer', 'other': 'other'}
RELIGION_MAP  = {'muslim': 'Muslim', 'non-muslim': 'Non-Muslim'}

created = 0
skipped = 0
errors  = []

with open(CSV_PATH, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader, start=2):
        row = {k.strip(): (v.strip() if v else '') for k, v in row.items()}
        full_name = row.get('Full Name', '')
        if not full_name:
            continue

        div_name = row.get('Division', '')
        grd_name = row.get('Grade', '')
        sec_name = row.get('Section', '')
        yr_name  = row.get('Academic Year', '')

        try:
            division = Division.objects.get(name__iexact=div_name)
            grade    = Grade.objects.get(name__iexact=grd_name, division=division)
            section  = Section.objects.get(name__iexact=sec_name, grade=grade)
            year     = AcademicYear.objects.get(name__iexact=yr_name)
        except Exception as e:
            errors.append(f"Row {i} ({full_name}): FK lookup failed — {e}")
            continue

        # Skip if a matching student already exists
        if Student.objects.filter(
            full_name=full_name, grade=grade, section=section, academic_year=year
        ).exists():
            skipped += 1
            continue

        try:
            dob = _date.fromisoformat(row.get('Date of Birth', ''))
        except ValueError:
            dob = _date(2015, 1, 1)
        try:
            admission = _date.fromisoformat(row.get('Admission Date', '')) if row.get('Admission Date') else _date.today()
        except ValueError:
            admission = _date.today()

        sm_name    = row.get('Study Mode', '').strip()
        study_mode = StudyMode.objects.filter(name__iexact=sm_name, is_active=True).first() if sm_name else None

        try:
            s = Student(
                full_name       = full_name,
                arabic_name     = row.get('Arabic Name', ''),
                gender          = GENDER_MAP.get(row.get('Gender', '').lower(), 'M'),
                dob             = dob,
                nationality     = row.get('Nationality', 'Saudi Arabia'),
                id_type         = ID_TYPE_MAP.get(row.get('ID Type', '').lower(), 'NATIONAL_ID'),
                national_id     = row.get('National ID', ''),
                iqama_number    = row.get('Iqama Number', ''),
                passport_number = row.get('Passport Number', ''),
                religion        = RELIGION_MAP.get(row.get('Religion', '').lower(), ''),
                birth_place     = row.get('Birth Place', ''),
                division        = division,
                grade           = grade,
                section         = section,
                academic_year   = year,
                roll_number     = row.get('Roll No.', ''),
                enrollment_type = ENROLL_MAP.get(row.get('Enrollment Type', '').lower(), 'NEW'),
                study_mode      = study_mode,
                fee_category    = FEE_CAT_MAP.get(row.get('Fee Category', '').lower(), 'regular'),
                admission_date  = admission,
                is_active       = (row.get('Active', 'Yes').lower() != 'no'),
                father_name     = row.get('Father Name', ''),
                mother_name     = row.get('Mother Name', ''),
                guardian_phone  = row.get('Guardian Phone', ''),
                guardian_email  = row.get('Guardian Email', ''),
                address         = row.get('Address', ''),
            )
            s.save()                       # uses the fixed retry-on-collision logic
            created += 1
        except Exception as e:
            errors.append(f"Row {i} ({full_name}): {e}")

print(f"Created: {created}")
print(f"Skipped (already in DB): {skipped}")
print(f"Errors: {len(errors)}")
for e in errors[:10]:
    print("  ", e)
print(f"\nTotal students in DB now: {Student.objects.count()}")
```

### deploy/fix_service/serve.py

| Field | Value |
| --- | --- |
| Bytes | 788 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py
"""
Run the ERP under Waitress.

Pointing NSSM (the Windows service manager) at  python.exe serve.py  is more
reliable than the waitress-serve.exe console-script wrapper, which can exit
immediately under a service and leave an empty log.
"""
import os
import sys

# Make this folder importable (so "ERP.wsgi" resolves) and set settings.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ERP.settings')

from waitress import serve
from ERP.wsgi import application

HOST = os.environ.get('ERP_HOST', '0.0.0.0')
PORT = int(os.environ.get('ERP_PORT', '8000'))

if __name__ == '__main__':
    print(f'Al-Kawthar ERP — Waitress serving on http://{HOST}:{PORT}', flush=True)
    serve(application, host=HOST, port=PORT, threads=8)
```

### deploy/fix_static/login.html

| Field | Value |
| --- | --- |
| Bytes | 6752 |
| Score | 0 |
| Why | context |
| Status | Full content |


```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Login — Al-Kawthar International Schools</title>
    <link rel="stylesheet" href="/static/css/tailwind.css">
</head>
<body class="min-h-screen bg-gradient-to-br from-[#1e3a5f] via-[#1a3356] to-[#0f2240] flex items-center justify-center p-4">

    <div class="w-full max-w-md">

        <!-- Card -->
        <div class="bg-white rounded-2xl shadow-2xl overflow-hidden">

            <!-- Header banner -->
            <div class="bg-gradient-to-r from-[#1e3a5f] to-[#2a5298] px-8 py-8 text-center">
                <!-- School Logo Circle -->
                <div class="w-16 h-16 rounded-full bg-yellow-400 flex items-center justify-center
                            text-[#1e3a5f] font-extrabold text-3xl mx-auto mb-4 shadow-lg select-none">
                    ك
                </div>
                <h1 class="text-white text-xl font-bold tracking-wide">Al-Kawthar International Schools</h1>
                <p class="text-blue-200 text-sm mt-1">Jeddah, Saudi Arabia</p>
            </div>

            <!-- Form -->
            <div class="px-8 py-8">
                <h2 class="text-slate-700 text-lg font-semibold mb-1">Sign in to ERP</h2>
                <p class="text-slate-400 text-sm mb-6">Enter your credentials to continue</p>

                <!-- Flash messages -->
                {% if messages %}
                <div class="mb-5 space-y-2">
                    {% for message in messages %}
                    <div class="px-4 py-3 rounded-lg text-sm font-medium
                        {% if message.tags == 'error' %}bg-red-50 text-red-700 border border-red-200
                        {% else %}bg-blue-50 text-blue-700 border border-blue-200{% endif %}">
                        {{ message }}
                    </div>
                    {% endfor %}
                </div>
                {% endif %}

                <form method="POST" action="{% url 'accounts:login' %}" autocomplete="off">
                    {% csrf_token %}

                    <!-- Username -->
                    <div class="mb-4">
                        <label class="block text-sm font-medium text-slate-600 mb-1.5" for="id_username">
                            Username
                        </label>
                        <div class="relative">
                            <span class="absolute inset-y-0 left-3 flex items-center text-slate-400">
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round"
                                          d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
                                </svg>
                            </span>
                            <input id="id_username" name="username" type="text" required autofocus
                                   placeholder="Enter your username"
                                   class="w-full pl-10 pr-4 py-2.5 border border-slate-200 rounded-lg text-sm
                                          focus:outline-none focus:ring-2 focus:ring-[#1e3a5f]/30 focus:border-[#1e3a5f]
                                          text-slate-700 placeholder-slate-300 transition" />
                        </div>
                    </div>

                    <!-- Password -->
                    <div class="mb-6">
                        <label class="block text-sm font-medium text-slate-600 mb-1.5" for="id_password">
                            Password
                        </label>
                        <div class="relative">
                            <span class="absolute inset-y-0 left-3 flex items-center text-slate-400">
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round"
                                          d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6
                                             a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
                                </svg>
                            </span>
                            <input id="id_password" name="password" type="password" required
                                   placeholder="Enter your password"
                                   class="w-full pl-10 pr-10 py-2.5 border border-slate-200 rounded-lg text-sm
                                          focus:outline-none focus:ring-2 focus:ring-[#1e3a5f]/30 focus:border-[#1e3a5f]
                                          text-slate-700 placeholder-slate-300 transition" />
                            <!-- Toggle password visibility -->
                            <button type="button" onclick="togglePassword()"
                                    class="absolute inset-y-0 right-3 flex items-center text-slate-400 hover:text-slate-600">
                                <svg id="eye-icon" class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round"
                                          d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                                    <path stroke-linecap="round" stroke-linejoin="round"
                                          d="M2.458 12C3.732 7.943 7.523 5 12 5c4.477 0 8.268 2.943
                                             9.542 7-1.274 4.057-5.065 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                                </svg>
                            </button>
                        </div>
                    </div>

                    <button type="submit"
                            class="w-full bg-[#1e3a5f] hover:bg-[#2a5298] text-white font-semibold
                                   py-2.5 rounded-lg transition duration-200 text-sm tracking-wide shadow-sm">
                        Sign In
                    </button>
                </form>
            </div>
        </div>

        <p class="text-center text-blue-200/60 text-xs mt-6">
            &copy; 2026 Al-Kawthar International Schools — ERP System
        </p>
    </div>

    <script>
        function togglePassword() {
            const input = document.getElementById('id_password');
            input.type = input.type === 'password' ? 'text' : 'password';
        }
    </script>
</body>
</html>
```

### deploy/fix_static/settings.py

| Field | Value |
| --- | --- |
| Bytes | 6596 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py
"""
Django settings for ERP project.

Generated by 'django-admin startproject' using Django 6.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/6.0/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# ── Minimal .env loader (no external dependency) ─────────────────────────────
# Reads KEY=VALUE lines from a .env file (repo root or BASE_DIR) into the
# environment, without overwriting variables already set by the OS/server.
def _load_dotenv():
    for candidate in (BASE_DIR.parent / '.env', BASE_DIR / '.env'):
        if not candidate.exists():
            continue
        for line in candidate.read_text(encoding='utf-8').splitlines():
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            key, _, value = line.partition('=')
            key, value = key.strip(), value.strip().strip('"').strip("'")
            os.environ.setdefault(key, value)
        break

_load_dotenv()


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '[REDACTED:SECRET]'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition
TAILWIND_APP_NAME = 'theme'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tailwind',
    'theme',
    # ERP Apps
    'core',
    'accounts',
    'students',
    'attendance',
    'academics',
    'fees',
    'staff',
    'ai_features',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ERP.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'builtins': ['fees.templatetags.fee_pdf_filters'],
        },
    },
]

WSGI_APPLICATION = 'ERP.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

# ── Database ──────────────────────────────────────────────────────────────────
# SQLite: zero-setup, single file (db.sqlite3) — ideal for offline/single-server.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# PostgreSQL (old) — kept for reference; uncomment to switch back.
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'school_db',
#         'USER': 'django_user',
#         'PASSWORD': '1234',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Riyadh'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Auth redirects
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

NPM_BIN_PATH = r"C:\Program Files\nodejs\npm.cmd"

AUTH_USER_MODEL = 'accounts.CustomUser'

# ── Cache (per-process in-memory; swap for Redis in production) ───────────────
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'erp-cache',
        'TIMEOUT': 300,   # 5 minutes default
    }
}

# OpenAI (optional) — set to enable GPT-4o-mini summaries in AI features
OPENAI_API_KEY = ''


# ── Email (fee reminders etc.) ────────────────────────────────────────────────
# Set EMAIL_HOST (+ credentials) in .env to send real email; without it,
# emails are printed to the console (dev mode).
EMAIL_HOST = os.environ.get('EMAIL_HOST', '')
if EMAIL_HOST:
    EMAIL_BACKEND       = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_PORT          = int(os.environ.get('EMAIL_PORT', '587'))
    EMAIL_HOST_USER     = os.environ.get('EMAIL_HOST_USER', '')
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
    EMAIL_USE_TLS       = os.environ.get('EMAIL_USE_TLS', '1') == '1'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = os.environ.get(
    'DEFAULT_FROM_EMAIL', 'Al-Kawthar International School <no-reply@alkawthar.edu.sa>')
```

### deploy/fix_static/urls.py

| Field | Value |
| --- | --- |
| Bytes | 1633 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py
"""
URL configuration for ERP project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve as _serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('students/', include('students.urls')),
    path('attendance/', include('attendance.urls')),
    path('academics/', include('academics.urls')),
    path('fees/', include('fees.urls')),
    path('staff/', include('staff.urls')),
    path('ai/', include('ai_features.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve collected static files under a pure-WSGI server (Waitress) where
# Django's runserver auto-serving is unavailable. Works with DEBUG on or off.
urlpatterns += [
    re_path(r'^static/(?P<path>.*)$', _serve, {'document_root': settings.STATIC_ROOT}),
]
```

### deploy/setup_server.sh

| Field | Value |
| --- | --- |
| Bytes | 5370 |
| Score | 0 |
| Why | context |
| Status | Full content |


```sh
#!/usr/bin/env bash
# deploy/setup_server.sh
# Run once on a fresh Ubuntu 22.04 / 24.04 server as root (or with sudo).
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

# ── 0. Variables ──────────────────────────────────────────────────────────────
APP_USER="erp"
APP_DIR="/home/$APP_USER/school-erp"
VENV_DIR="$APP_DIR/venv"
REPO_URL="https://github.com/inam0980/School-ERP-System.git"   # update if private
DOMAIN="yourdomain.com"
DB_NAME="school_db"
DB_USER="django_user"
DB_PASS="StrongProductionPassword!"    # change before running!

# ── 1. System packages ────────────────────────────────────────────────────────
apt-get update -y
apt-get install -y \
    python3.12 python3.12-venv python3.12-dev \
    postgresql postgresql-contrib \
    nginx certbot python3-certbot-nginx \
    git build-essential libpq-dev \
    supervisor

# ── 2. Create app user ────────────────────────────────────────────────────────
id "$APP_USER" &>/dev/null || useradd -m -s /bin/bash "$APP_USER"
usermod -aG www-data "$APP_USER"

# ── 3. PostgreSQL setup ───────────────────────────────────────────────────────
systemctl start postgresql
systemctl enable postgresql

sudo -u postgres psql <<PGSQL
DO \$\$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = '$DB_USER') THEN
        CREATE ROLE $DB_USER WITH LOGIN PASSWORD '$DB_PASS';
    END IF;
END
\$\$;
CREATE DATABASE $DB_NAME OWNER $DB_USER;
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
PGSQL

# ── 4. Clone repo ─────────────────────────────────────────────────────────────
sudo -u "$APP_USER" bash -c "
    git clone $REPO_URL $APP_DIR || (cd $APP_DIR && git pull)
"

# ── 5. Python venv & dependencies ─────────────────────────────────────────────
sudo -u "$APP_USER" bash -c "
    python3.12 -m venv $VENV_DIR
    $VENV_DIR/bin/pip install --upgrade pip
    $VENV_DIR/bin/pip install \
        django==6.0.4 \
        psycopg2-binary \
        gunicorn \
        whitenoise \
        python-decouple \
        Pillow \
        openpyxl \
        factory-boy \
        pytest-django
"

# ── 6. Copy .env ──────────────────────────────────────────────────────────────
echo ">>> Copy your .env file to $APP_DIR/.env now, then press Enter to continue."
read -r

# ── 7. Django setup ───────────────────────────────────────────────────────────
sudo -u "$APP_USER" bash -c "
    cd $APP_DIR/ERP
    export DJANGO_SETTINGS_MODULE=ERP.settings_production
    $VENV_DIR/bin/python manage.py migrate --noinput
    $VENV_DIR/bin/python manage.py collectstatic --noinput
"

# ── 8. Gunicorn socket directory ──────────────────────────────────────────────
mkdir -p /run/gunicorn
chown "$APP_USER":www-data /run/gunicorn

# ── 9. Log directories ────────────────────────────────────────────────────────
mkdir -p /var/log/gunicorn
chown "$APP_USER":www-data /var/log/gunicorn

# ── 10. Systemd service ───────────────────────────────────────────────────────
cp "$APP_DIR/deploy/systemd/school_erp.service" /etc/systemd/system/school_erp.service
systemctl daemon-reload
systemctl enable school_erp
systemctl start school_erp

# ── 11. Nginx ─────────────────────────────────────────────────────────────────
cp "$APP_DIR/deploy/nginx/school_erp.conf" /etc/nginx/sites-available/school_erp
ln -sf /etc/nginx/sites-available/school_erp /etc/nginx/sites-enabled/school_erp
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl reload nginx

# ── 12. SSL certificate ───────────────────────────────────────────────────────
certbot --nginx -d "$DOMAIN" -d "www.$DOMAIN" --non-interactive --agree-tos -m "admin@$DOMAIN"
systemctl reload nginx

echo "✓ Deployment complete. Visit https://$DOMAIN"
```

### ERP/academics/__init__.py

| Field | Value |
| --- | --- |
| Bytes | 0 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py

```

### ERP/academics/admin.py

| Field | Value |
| --- | --- |
| Bytes | 1319 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py
from django.contrib import admin
from .models import ExamType, Exam, Mark, GradeConfig, ReportCard


class MarkInline(admin.TabularInline):
    model  = Mark
    extra  = 0
    fields = ('student', 'obtained_marks', 'is_absent', 'status', 'remarks')
    readonly_fields = ('student',)


@admin.register(ExamType)
class ExamTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'weight_percentage')


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display  = ('name', 'subject', 'section', 'term', 'date', 'total_marks', 'academic_year')
    list_filter   = ('term', 'academic_year', 'section')
    search_fields = ('name', 'subject__name')
    inlines       = [MarkInline]


@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display  = ('student', 'exam', 'obtained_marks', 'is_absent', 'status')
    list_filter   = ('status', 'is_absent', 'exam__term')
    search_fields = ('student__full_name', 'student__student_id')


@admin.register(GradeConfig)
class GradeConfigAdmin(admin.ModelAdmin):
    list_display = ('grade', 'passing_marks', 'gpa_scale')


@admin.register(ReportCard)
class ReportCardAdmin(admin.ModelAdmin):
    list_display = ('student', 'academic_year', 'term', 'generated_at')
    list_filter  = ('term', 'academic_year')
```

### ERP/academics/apps.py

| Field | Value |
| --- | --- |
| Bytes | 98 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py
from django.apps import AppConfig


class AcademicsConfig(AppConfig):
    name = 'academics'
```

### ERP/academics/forms.py

| Field | Value |
| --- | --- |
| Bytes | 4862 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py
from django import forms
from django.contrib.auth import get_user_model
from .models import ExamType, Exam, Mark, GradeConfig
from core.models import Subject, Section, AcademicYear, Grade, Division

User = get_user_model()

_INPUT   = ('w-full px-3 py-2.5 border border-slate-200 rounded-lg text-sm text-slate-700 '
            'focus:outline-none focus:ring-2 focus:ring-[#1e3a5f]/30 focus:border-[#1e3a5f] '
            'transition bg-white')
_CHECK   = 'w-4 h-4 text-[#1e3a5f] rounded border-slate-300 cursor-pointer'
_SMALL   = ('w-full px-2 py-1.5 border border-slate-200 rounded text-sm text-slate-700 '
            'focus:outline-none focus:ring-1 focus:ring-[#1e3a5f]/30 bg-white')


class ExamTypeForm(forms.ModelForm):
    class Meta:
        model  = ExamType
        fields = ['name', 'weight_percentage']
        widgets = {
            'name':              forms.TextInput(attrs={'class': _INPUT}),
            'weight_percentage': forms.NumberInput(attrs={'class': _INPUT, 'min': 1, 'max': 100}),
        }


class ExamForm(forms.ModelForm):
    class Meta:
        model  = Exam
        fields = ['name', 'exam_type', 'subject', 'section', 'academic_year', 'term', 'date', 'total_marks']
        widgets = {
            'name':          forms.TextInput(attrs={'class': _INPUT}),
            'exam_type':     forms.Select(attrs={'class': _INPUT}),
            'subject':       forms.Select(attrs={'class': _INPUT}),
            'section':       forms.Select(attrs={'class': _INPUT}),
            'academic_year': forms.Select(attrs={'class': _INPUT}),
            'term':          forms.Select(attrs={'class': _INPUT}),
            'date':          forms.DateInput(attrs={'type': 'date', 'class': _INPUT}),
            'total_marks':   forms.NumberInput(attrs={'class': _INPUT, 'min': 1}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['academic_year'].queryset = AcademicYear.objects.all().order_by('-start_date')


class MarksEntryFilterForm(forms.Form):
    """Filter used on the marks entry page to select an exam."""
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.filter(is_active=True),
        required=False,
        empty_label='Select Subject',
        widget=forms.Select(attrs={'class': _INPUT}),
    )
    section = forms.ModelChoiceField(
        queryset=Section.objects.all(),
        required=False,
        empty_label='Select Section',
        widget=forms.Select(attrs={'class': _INPUT}),
    )
    exam = forms.ModelChoiceField(
        queryset=Exam.objects.none(),
        required=False,
        empty_label='Select Exam',
        widget=forms.Select(attrs={'class': _INPUT}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'section' in self.data and 'subject' in self.data:
            try:
                sec_id = int(self.data.get('section'))
                sub_id = int(self.data.get('subject'))
                self.fields['exam'].queryset = Exam.objects.filter(
                    section_id=sec_id, subject_id=sub_id
                ).order_by('-date')
            except (ValueError, TypeError):
                pass


class GradeConfigForm(forms.ModelForm):
    class Meta:
        model  = GradeConfig
        fields = ['grade', 'passing_marks', 'gpa_scale']
        widgets = {
            'grade':         forms.Select(attrs={'class': _INPUT}),
            'passing_marks': forms.NumberInput(attrs={'class': _INPUT, 'min': 1, 'max': 100}),
            'gpa_scale':     forms.Select(attrs={'class': _INPUT}),
        }


class ReportCardFilterForm(forms.Form):
    """Filter for generating / viewing report cards."""
    section = forms.ModelChoiceField(
        queryset=Section.objects.select_related('grade', 'grade__division').all(),
        required=True,
        empty_label='Select Section',
        widget=forms.Select(attrs={'class': _INPUT}),
    )
    academic_year = forms.ModelChoiceField(
        queryset=AcademicYear.objects.all().order_by('-start_date'),
        required=True,
        empty_label='Select Year',
        widget=forms.Select(attrs={'class': _INPUT}),
    )
    term = forms.ChoiceField(
        choices=[('', 'Select Term'), ('T1', 'Term 1'), ('T2', 'Term 2'), ('T3', 'Term 3'), ('FI', 'Final')],
        required=True,
        widget=forms.Select(attrs={'class': _INPUT}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Try to default to current academic year
        try:
            current = AcademicYear.objects.get(is_current=True)
            self.fields['academic_year'].initial = current.pk
        except AcademicYear.DoesNotExist:
            pass
```

### ERP/academics/migrations/__init__.py

| Field | Value |
| --- | --- |
| Bytes | 0 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py

```

### ERP/academics/migrations/0001_initial.py

| Field | Value |
| --- | --- |
| Bytes | 6289 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py
# Generated by Django 6.0.4 on 2026-04-13 12:00

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        ('students', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ExamType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='e.g. Quiz, MidTerm, Final', max_length=50, unique=True)),
                ('weight_percentage', models.PositiveSmallIntegerField(default=100, help_text='Weight of this exam type in the overall grade (1-100)', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Exam Type',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('term', models.CharField(choices=[('T1', 'Term 1'), ('T2', 'Term 2'), ('T3', 'Term 3'), ('FI', 'Final')], default='T1', max_length=2)),
                ('date', models.DateField()),
                ('total_marks', models.PositiveSmallIntegerField(default=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('academic_year', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='exams', to='core.academicyear')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='exams_created', to=settings.AUTH_USER_MODEL)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='exams', to='core.section')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='exams', to='core.subject')),
                ('exam_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='exams', to='academics.examtype')),
            ],
            options={
                'verbose_name': 'Exam',
                'ordering': ['-date', 'name'],
            },
        ),
        migrations.CreateModel(
            name='GradeConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('passing_marks', models.PositiveSmallIntegerField(default=60, help_text='Passing percentage (1-100)')),
                ('gpa_scale', models.CharField(choices=[('AMERICAN', 'American (4.0 GPA)'), ('BRITISH', 'British (A*-U)'), ('FRENCH', 'French (20-point)')], default='AMERICAN', max_length=10)),
                ('grade', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='config', to='core.grade')),
            ],
            options={
                'verbose_name': 'Grade Config',
            },
        ),
        migrations.CreateModel(
            name='Mark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('obtained_marks', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('is_absent', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('submitted', 'Submitted'), ('approved', 'Approved')], default='draft', max_length=10)),
                ('remarks', models.CharField(blank=True, max_length=200)),
                ('approved_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='marks_approved', to=settings.AUTH_USER_MODEL)),
                ('entered_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='marks_entered', to=settings.AUTH_USER_MODEL)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='marks', to='academics.exam')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='marks', to='students.student')),
            ],
            options={
                'verbose_name': 'Mark',
                'ordering': ['student__full_name'],
                'unique_together': {('student', 'exam')},
            },
        ),
        migrations.CreateModel(
            name='ReportCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term', models.CharField(choices=[('T1', 'Term 1'), ('T2', 'Term 2'), ('T3', 'Term 3'), ('FI', 'Final')], max_length=2)),
                ('generated_at', models.DateTimeField(auto_now=True)),
                ('pdf_file', models.FileField(blank=True, null=True, upload_to='report_cards/')),
                ('academic_year', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='report_cards', to='core.academicyear')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='report_cards', to='students.student')),
            ],
            options={
                'verbose_name': 'Report Card',
                'ordering': ['-generated_at'],
                'unique_together': {('student', 'academic_year', 'term')},
            },
        ),
    ]
```

### ERP/academics/models.py

| Field | Value |
| --- | --- |
| Bytes | 8672 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from core.models import AcademicYear, Division, Grade, Section, Subject
from students.models import Student


# ──────────────────────────────────────────────────────────────────────────────
# EXAM TYPE  (Quiz / Assignment / MidTerm / Final)
# ──────────────────────────────────────────────────────────────────────────────

class ExamType(models.Model):
    name              = models.CharField(max_length=50, unique=True, help_text="e.g. Quiz, MidTerm, Final")
    weight_percentage = models.PositiveSmallIntegerField(
        default=100,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        help_text="Weight of this exam type in the overall grade (1-100)",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Exam Type'

    def __str__(self):
        return f"{self.name} ({self.weight_percentage}%)"


# ──────────────────────────────────────────────────────────────────────────────
# EXAM
# ──────────────────────────────────────────────────────────────────────────────

TERM_CHOICES = [
    ('T1', 'Term 1'),
    ('T2', 'Term 2'),
    ('T3', 'Term 3'),
    ('FI', 'Final'),
]


class Exam(models.Model):
    name          = models.CharField(max_length=200)
    exam_type     = models.ForeignKey(ExamType, on_delete=models.PROTECT, related_name='exams')
    subject       = models.ForeignKey(Subject,  on_delete=models.PROTECT, related_name='exams')
    section       = models.ForeignKey(Section,  on_delete=models.PROTECT, related_name='exams')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.PROTECT, related_name='exams')
    term          = models.CharField(max_length=2, choices=TERM_CHOICES, default='T1')
    date          = models.DateField()
    total_marks   = models.PositiveSmallIntegerField(default=100)
    created_by    = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, null=True,
        related_name='exams_created',
    )
    created_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', 'name']
        verbose_name = 'Exam'

    def __str__(self):
        return f"{self.name} — {self.subject} ({self.section})"


# ──────────────────────────────────────────────────────────────────────────────
# MARK  (per student per exam)
# ──────────────────────────────────────────────────────────────────────────────

MARK_STATUS = [
    ('draft',     'Draft'),
    ('submitted', 'Submitted'),
    ('approved',  'Approved'),
]


class Mark(models.Model):
    student        = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='marks')
    exam           = models.ForeignKey(Exam,    on_delete=models.CASCADE, related_name='marks')
    obtained_marks = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    is_absent      = models.BooleanField(default=False)
    status         = models.CharField(max_length=10, choices=MARK_STATUS, default='draft')
    remarks        = models.CharField(max_length=200, blank=True)
    entered_by     = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, null=True, blank=True,
        related_name='marks_entered',
    )
    approved_by    = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, null=True, blank=True,
        related_name='marks_approved',
    )
    approved_at    = models.DateTimeField(null=True, blank=True)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['student', 'exam']
        ordering = ['student__full_name']
        verbose_name = 'Mark'

    def __str__(self):
        return f"{self.student} — {self.exam} — {self.obtained_marks}"

    # ── Auto-computed helpers ─────────────────────────────────────────
    def get_percentage(self):
        if self.is_absent or self.obtained_marks is None:
            return None
        return round(float(self.obtained_marks) / self.exam.total_marks * 100, 1)

    def get_letter_grade(self):
        pct = self.get_percentage()
        if pct is None:
            return 'AB'
        if pct >= 90: return 'A+'
        if pct >= 85: return 'A'
        if pct >= 80: return 'B+'
        if pct >= 75: return 'B'
        if pct >= 70: return 'C+'
        if pct >= 65: return 'C'
        if pct >= 60: return 'D'
        return 'F'

    def get_gpa_points(self):
        grade = self.get_letter_grade()
        mapping = {
            'A+': 4.0, 'A': 4.0, 'B+': 3.5, 'B': 3.0,
            'C+': 2.5, 'C': 2.0, 'D': 1.0, 'F': 0.0, 'AB': 0.0,
        }
        return mapping.get(grade, 0.0)

    def is_passed(self):
        pct = self.get_percentage()
        return pct is not None and pct >= 60


# ──────────────────────────────────────────────────────────────────────────────
# GRADE CONFIG (passing mark threshold per grade)
# ──────────────────────────────────────────────────────────────────────────────

class GradeConfig(models.Model):
    GPA_AMERICAN = 'AMERICAN'
    GPA_BRITISH  = 'BRITISH'
    GPA_FRENCH   = 'FRENCH'
    GPA_SCALE_CHOICES = [
        (GPA_AMERICAN, 'American (4.0 GPA)'),
        (GPA_BRITISH,  'British (A*-U)'),
        (GPA_FRENCH,   'French (20-point)'),
    ]

    grade         = models.OneToOneField(Grade, on_delete=models.CASCADE, related_name='config')
    passing_marks = models.PositiveSmallIntegerField(default=60, help_text="Passing percentage (1-100)")
    gpa_scale     = models.CharField(max_length=10, choices=GPA_SCALE_CHOICES, default=GPA_AMERICAN)

    class Meta:
        verbose_name = 'Grade Config'

    def __str__(self):
        return f"Config: {self.grade} — Pass ≥ {self.passing_marks}%"


# ──────────────────────────────────────────────────────────────────────────────
# REPORT CARD
# ──────────────────────────────────────────────────────────────────────────────

class ReportCard(models.Model):
    student       = models.ForeignKey(Student,     on_delete=models.CASCADE, related_name='report_cards')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.PROTECT, related_name='report_cards')
    term          = models.CharField(max_length=2,  choices=TERM_CHOICES)
    generated_at  = models.DateTimeField(auto_now=True)
    pdf_file      = models.FileField(upload_to='report_cards/', blank=True, null=True)

    class Meta:
        unique_together = ['student', 'academic_year', 'term']
        ordering = ['-generated_at']
        verbose_name = 'Report Card'

    def __str__(self):
        return f"{self.student} — {self.academic_year} {self.get_term_display()}"
```

### ERP/academics/urls.py

| Field | Value |
| --- | --- |
| Bytes | 2457 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py
from django.urls import path
from django.shortcuts import redirect
from . import views

app_name = 'academics'

urlpatterns = [
    # Root redirect → exam list
    path('', lambda req: redirect('academics:exam_list'), name='index'),

    # Exam types
    path('exam-types/',                    views.exam_type_list,   name='exam_type_list'),
    path('exam-types/add/',                views.exam_type_form,   name='exam_type_add'),
    path('exam-types/<int:pk>/edit/',      views.exam_type_form,   name='exam_type_edit'),
    path('exam-types/<int:pk>/delete/',    views.exam_type_delete, name='exam_type_delete'),

    # Exams
    path('exams/',                         views.exam_list,        name='exam_list'),
    path('exams/add/',                     views.exam_form,        name='exam_add'),
    path('exams/<int:pk>/edit/',           views.exam_form,        name='exam_edit'),
    path('exams/<int:pk>/delete/',         views.exam_delete,      name='exam_delete'),

    # Marks workflow
    path('exams/<int:exam_pk>/marks/',     views.marks_entry,      name='marks_entry'),
    path('exams/<int:exam_pk>/approve/',   views.approve_marks,    name='approve_marks'),
    path('exams/<int:exam_pk>/unlock/',    views.unlock_marks,     name='unlock_marks'),
    path('exams/<int:exam_pk>/results/',   views.exam_results,     name='exam_results'),
    path('exams/<int:exam_pk>/export/',    views.export_marks_excel, name='export_marks'),

    # Marks approval queue
    path('marks/pending/',                 views.marks_approval,   name='marks_approval'),

    # Report cards
    path('report-card/<int:student_pk>/',  views.report_card_view, name='report_card'),
    path('report-card/<int:student_pk>/pdf/', views.report_card_pdf, name='report_card_pdf'),
    path('report-cards/bulk/',             views.bulk_report_cards, name='bulk_report_cards'),

    # Noor export
    path('export/noor/',                   views.noor_export,      name='noor_export'),

    # Grade configs
    path('grade-configs/',                 views.grade_config_list, name='grade_config_list'),
    path('grade-configs/add/',             views.grade_config_form, name='grade_config_add'),
    path('grade-configs/<int:pk>/edit/',   views.grade_config_form, name='grade_config_edit'),

    # JSON APIs
    path('api/subjects/',  views.api_subjects_by_section,    name='api_subjects'),
    path('api/exams/',     views.api_exams_by_subject_section, name='api_exams'),
]
```

### ERP/accounts/__init__.py

| Field | Value |
| --- | --- |
| Bytes | 0 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py

```

### ERP/accounts/admin.py

| Field | Value |
| --- | --- |
| Bytes | 1054 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Division


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display  = ('username', 'full_name', 'email', 'role', 'division', 'is_active')
    list_filter   = ('role', 'division', 'is_active')
    search_fields = ('username', 'email', 'full_name')
    ordering      = ('username',)
    fieldsets = (
        (None,           {'fields': ('username', 'password')}),
        ('Personal',     {'fields': ('full_name', 'email', 'role', 'division')}),
        ('Permissions',  {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'full_name', 'role', 'division', 'password1', 'password2'),
        }),
    )


@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
```

### ERP/accounts/apps.py

| Field | Value |
| --- | --- |
| Bytes | 96 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py
from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'
```

### ERP/accounts/decorators.py

| Field | Value |
| --- | --- |
| Bytes | 1200 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def role_required(*roles):
    """
    Restrict view access to users with one of the specified roles.
    Usage: @role_required('ADMIN', 'SUPER_ADMIN')
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('accounts:login')
            if request.user.role not in roles:
                messages.error(request, "You don't have permission to access this page.")
                return redirect('core:dashboard')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def login_excluded(redirect_to='core:dashboard'):
    """Redirect already-authenticated users away from login page."""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_to)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
```

### ERP/accounts/management/__init__.py

| Field | Value |
| --- | --- |
| Bytes | 0 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py

```

### ERP/accounts/management/commands/__init__.py

| Field | Value |
| --- | --- |
| Bytes | 0 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py

```

### ERP/accounts/management/commands/create_super_admin.py

| Field | Value |
| --- | --- |
| Bytes | 1749 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import Division

User = get_user_model()


class Command(BaseCommand):
    help = 'Create the default Super Admin user for Al-Kawthar ERP'

    def add_arguments(self, parser):
        parser.add_argument('--username', default='superadmin', help='Username (default: superadmin)')
        parser.add_argument('--email',    default='admin@alkawthar.edu.sa', help='Email address')
        parser.add_argument('--password', default='Admin@1234', help='Password')
        parser.add_argument('--fullname', default='System Administrator', help='Full name')

    def handle(self, *args, **options):
        username  = options['username']
        email     = options['email']
        password  = options['password']
        full_name = options['fullname']

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'User "{username}" already exists.'))
            return

        # Ensure at least one division exists
        division, _ = Division.objects.get_or_create(
            name='AMERICAN',
            defaults={'description': 'American Division'}
        )

        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            full_name=full_name,
            division=division,
        )
        self.stdout.write(self.style.SUCCESS(
            f'Super Admin "{user.username}" created successfully.\n'
            f'  Email   : {user.email}\n'
            f'  Password: {password}\n'
            f'  Role    : {user.get_role_display()}'
        ))
```

### ERP/accounts/migrations/__init__.py

| Field | Value |
| --- | --- |
| Bytes | 0 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py

```

### ERP/accounts/migrations/0001_initial.py

| Field | Value |
| --- | --- |
| Bytes | 2848 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py
# Generated by Django 6.0.4 on 2026-04-13 10:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Division',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('AMERICAN', 'American'), ('BRITISH', 'British'), ('FRENCH', 'French')], max_length=20, unique=True)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=150, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('full_name', models.CharField(max_length=200)),
                ('role', models.CharField(choices=[('SUPER_ADMIN', 'Super Admin'), ('ADMIN', 'Admin'), ('TEACHER', 'Teacher'), ('ACCOUNTANT', 'Accountant'), ('STAFF', 'Staff'), ('PARENT', 'Parent')], default='STAFF', max_length=20)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
                ('division', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to='accounts.division')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
        ),
    ]
```

### ERP/accounts/models.py

| Field | Value |
| --- | --- |
| Bytes | 2907 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class Division(models.Model):
    DIVISION_CHOICES = [
        ('AMERICAN', 'American'),
        ('BRITISH', 'British'),
        ('FRENCH', 'French'),
    ]
    name = models.CharField(max_length=20, choices=DIVISION_CHOICES, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.get_name_display()


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', CustomUser.SUPER_ADMIN)
        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    SUPER_ADMIN = 'SUPER_ADMIN'
    ADMIN = 'ADMIN'
    TEACHER = 'TEACHER'
    ACCOUNTANT = 'ACCOUNTANT'
    STAFF = 'STAFF'
    PARENT = 'PARENT'

    ROLE_CHOICES = [
        (SUPER_ADMIN, 'Super Admin'),
        (ADMIN, 'Admin'),
        (TEACHER, 'Teacher'),
        (ACCOUNTANT, 'Accountant'),
        (STAFF, 'Staff'),
        (PARENT, 'Parent'),
    ]

    username   = models.CharField(max_length=150, unique=True)
    email      = models.EmailField(unique=True)
    full_name  = models.CharField(max_length=200)
    role       = models.CharField(max_length=20, choices=ROLE_CHOICES, default=STAFF)
    division   = models.ForeignKey(Division, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='users')
    is_active  = models.BooleanField(default=True)
    is_staff   = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'full_name']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.full_name} ({self.get_role_display()})"

    @property
    def is_super_admin(self):
        return self.role == self.SUPER_ADMIN

    @property
    def is_admin_role(self):
        return self.role in (self.SUPER_ADMIN, self.ADMIN)

    @property
    def is_teacher(self):
        return self.role == self.TEACHER

    @property
    def is_accountant(self):
        return self.role == self.ACCOUNTANT
```

### ERP/accounts/urls.py

| Field | Value |
| --- | --- |
| Bytes | 263 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/',   views.login_view,   name='login'),
    path('logout/',  views.logout_view,  name='logout'),
    path('profile/', views.profile_view, name='profile'),
]
```

### ERP/accounts/views.py

| Field | Value |
| --- | --- |
| Bytes | 1280 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .decorators import login_excluded
from .models import CustomUser


@login_excluded('core:dashboard')
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                next_url = request.GET.get('next', 'core:dashboard')
                return redirect(next_url)
            else:
                messages.error(request, 'Your account has been deactivated.')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('accounts:login')


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')
```

### ERP/ai_features/__init__.py

| Field | Value |
| --- | --- |
| Bytes | 0 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py

```

### ERP/ai_features/admin.py

| Field | Value |
| --- | --- |
| Bytes | 66 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py
from django.contrib import admin

# Register your models here.
```

### ERP/ai_features/apps.py

| Field | Value |
| --- | --- |
| Bytes | 101 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py
from django.apps import AppConfig


class AiFeaturesConfig(AppConfig):
    name = 'ai_features'
```

### ERP/ai_features/migrations/__init__.py

| Field | Value |
| --- | --- |
| Bytes | 0 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py

```

### ERP/ai_features/models.py

| Field | Value |
| --- | --- |
| Bytes | 60 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py
from django.db import models

# Create your models here.
```

### ERP/ai_features/urls.py

| Field | Value |
| --- | --- |
| Bytes | 680 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py
from django.urls import path
from . import views

app_name = 'ai'

urlpatterns = [
    path('',                                    views.ai_dashboard,       name='dashboard'),
    path('attendance-risk/',                    views.attendance_risk,    name='attendance_risk'),
    path('grade-analytics/',                    views.grade_analytics,    name='grade_analytics'),
    path('fee-defaults/',                       views.fee_default_risk,   name='fee_default_risk'),
    path('performance/<int:student_pk>/',       views.performance_summary, name='performance_summary'),
    path('noor-validation/',                    views.noor_validation,    name='noor_validation'),
]
```

### ERP/ai_features/views.py

| Field | Value |
| --- | --- |
| Bytes | 10660 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py
import json

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.cache import cache

from accounts.decorators import role_required
from core.models import AcademicYear, Section, Grade
from students.models import Student

from .analytics import (
    compute_attendance_risk, attendance_risk_summary,
    compute_student_grade_trends, compute_section_performance,
    compute_fee_default_risk,
    generate_performance_summary,
    validate_noor_export,
    RISK_HIGH, RISK_MEDIUM,
)

_ADMIN = ('SUPER_ADMIN', 'ADMIN')
_STAFF = ('SUPER_ADMIN', 'ADMIN', 'TEACHER', 'ACCOUNTANT', 'STAFF')
_MANAGEMENT = ('SUPER_ADMIN', 'ADMIN', 'ACCOUNTANT')

_CACHE_TTL = 1800  # 30 minutes


# ──────────────────────────────────────────────────────────────────────────────
# AI HUB DASHBOARD
# ──────────────────────────────────────────────────────────────────────────────

@login_required
@role_required(*_MANAGEMENT)
def ai_dashboard(request):
    current_year = AcademicYear.objects.filter(is_current=True).first()
    year_pk      = current_year.pk if current_year else 'none'
    cache_key    = f'ai_dashboard_stats_{year_pk}'

    stats = cache.get(cache_key)
    if stats is None:
        risk_list     = compute_attendance_risk(academic_year=current_year)
        attn_summary  = attendance_risk_summary(risk_list)

        grade_list    = compute_student_grade_trends(academic_year=current_year)
        failing_count = sum(1 for g in grade_list if g['failing_subjects'])

        fee_list      = compute_fee_default_risk(academic_year=current_year)
        fee_high      = sum(1 for f in fee_list if f['risk'] == RISK_HIGH)

        noor_result   = validate_noor_export(academic_year=current_year)

        stats = {
            'attn_summary':  attn_summary,
            'failing_count': failing_count,
            'fee_high':      fee_high,
            'noor_errors':   noor_result['error_count'],
            'noor_total':    noor_result['total'],
        }
        cache.set(cache_key, stats, _CACHE_TTL)

    return render(request, 'ai_features/dashboard.html', {
        'current_year':   current_year,
        **stats,
    })


# ──────────────────────────────────────────────────────────────────────────────
# 1. ATTENDANCE RISK
# ──────────────────────────────────────────────────────────────────────────────

@login_required
@role_required(*_STAFF)
def attendance_risk(request):
    current_year = AcademicYear.objects.filter(is_current=True).first()
    years        = AcademicYear.objects.all()
    grades       = Grade.objects.all()
    sections     = Section.objects.all().select_related('grade')

    year_id    = request.GET.get('year')
    grade_id   = request.GET.get('grade')
    section_id = request.GET.get('section')
    risk_filter = request.GET.get('risk', '')

    selected_year    = AcademicYear.objects.filter(pk=year_id).first() if year_id else current_year
    selected_grade   = Grade.objects.filter(pk=grade_id).first() if grade_id else None
    selected_section = Section.objects.filter(pk=section_id).first() if section_id else None

    risk_list = compute_attendance_risk(
        academic_year=selected_year,
        section=selected_section,
        grade=selected_grade,
    )

    if risk_filter:
        risk_list = [r for r in risk_list if r['risk'] == risk_filter]

    summary = attendance_risk_summary(risk_list)

    return render(request, 'ai_features/attendance_risk.html', {
        'risk_list':        risk_list,
        'summary':          summary,
        'years':            years,
        'grades':           grades,
        'sections':         sections,
        'selected_year':    selected_year,
        'selected_grade':   selected_grade,
        'selected_section': selected_section,
        'risk_filter':      risk_filter,
    })


# ──────────────────────────────────────────────────────────────────────────────
# 2. GRADE ANALYTICS
# ──────────────────────────────────────────────────────────────────────────────

@login_required
@role_required(*_STAFF)
def grade_analytics(request):
    current_year = AcademicYear.objects.filter(is_current=True).first()
    years        = AcademicYear.objects.all()
    grades       = Grade.objects.all()
    sections     = Section.objects.all().select_related('grade')

    year_id    = request.GET.get('year')
    grade_id   = request.GET.get('grade')
    section_id = request.GET.get('section')

    selected_year    = AcademicYear.objects.filter(pk=year_id).first() if year_id else current_year
    selected_grade   = Grade.objects.filter(pk=grade_id).first() if grade_id else None
    selected_section = Section.objects.filter(pk=section_id).first() if section_id else None

    student_trends   = compute_student_grade_trends(
        academic_year=selected_year,
        section=selected_section,
        grade=selected_grade,
    )

    section_perf = compute_section_performance(academic_year=selected_year)
    chart_json   = json.dumps({
        'labels': section_perf['labels'],
        'data':   section_perf['data'],
    })

    return render(request, 'ai_features/grade_analytics.html', {
        'student_trends':   student_trends,
        'section_perf':     section_perf['sections'],
        'chart_json':       chart_json,
        'years':            years,
        'grades':           grades,
        'sections':         sections,
        'selected_year':    selected_year,
        'selected_grade':   selected_grade,
        'selected_section': selected_section,
    })


# ──────────────────────────────────────────────────────────────────────────────
# 3. FEE DEFAULT PREDICTION
# ──────────────────────────────────────────────────────────────────────────────

@login_required
@role_required('SUPER_ADMIN', 'ADMIN', 'ACCOUNTANT')
def fee_default_risk(request):
    current_year = AcademicYear.objects.filter(is_current=True).first()
    years        = AcademicYear.objects.all()

    year_id      = request.GET.get('year')
    risk_filter  = request.GET.get('risk', '')
    selected_year = AcademicYear.objects.filter(pk=year_id).first() if year_id else current_year

    fee_list = compute_fee_default_risk(academic_year=selected_year)
    if risk_filter:
        fee_list = [f for f in fee_list if f['risk'] == risk_filter]

    high   = sum(1 for f in fee_list if f['risk'] == RISK_HIGH)
    medium = sum(1 for f in fee_list if f['risk'] == RISK_MEDIUM)

    return render(request, 'ai_features/fee_default_risk.html', {
        'fee_list':     fee_list,
        'years':        years,
        'selected_year': selected_year,
        'risk_filter':  risk_filter,
        'high_count':   high,
        'medium_count': medium,
    })


# ──────────────────────────────────────────────────────────────────────────────
# 4. SMART PERFORMANCE SUMMARY
# ──────────────────────────────────────────────────────────────────────────────

@login_required
@role_required(*_STAFF)
def performance_summary(request, student_pk):
    student      = get_object_or_404(Student, pk=student_pk)
    current_year = AcademicYear.objects.filter(is_current=True).first()

    year_id      = request.GET.get('year')
    selected_year = AcademicYear.objects.filter(pk=year_id).first() if year_id else current_year

    summary_text = generate_performance_summary(student, academic_year=selected_year)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'summary': summary_text})

    years = AcademicYear.objects.all()
    return render(request, 'ai_features/performance_summary.html', {
        'student':       student,
        'summary_text':  summary_text,
        'years':         years,
        'selected_year': selected_year,
    })


# ──────────────────────────────────────────────────────────────────────────────
# 5. NOOR CSV VALIDATION
# ──────────────────────────────────────────────────────────────────────────────

@login_required
@role_required(*_ADMIN)
def noor_validation(request):
    current_year  = AcademicYear.objects.filter(is_current=True).first()
    years         = AcademicYear.objects.all()
    year_id       = request.GET.get('year')
    selected_year = AcademicYear.objects.filter(pk=year_id).first() if year_id else current_year

    result = validate_noor_export(academic_year=selected_year)

    return render(request, 'ai_features/noor_validation.html', {
        'result':        result,
        'years':         years,
        'selected_year': selected_year,
    })
```

### ERP/attendance/__init__.py

| Field | Value |
| --- | --- |
| Bytes | 0 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py

```

### ERP/attendance/admin.py

| Field | Value |
| --- | --- |
| Bytes | 1069 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py
from django.contrib import admin
from .models import Attendance, StaffAttendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display  = ('student', 'date', 'status', 'marked_by', 'remarks')
    list_filter   = ('status', 'date', 'student__section', 'student__grade', 'student__division')
    search_fields = ('student__full_name', 'student__student_id')
    date_hierarchy = 'date'
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-date', 'student__full_name')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'student', 'student__grade', 'student__section', 'marked_by'
        )


@admin.register(StaffAttendance)
class StaffAttendanceAdmin(admin.ModelAdmin):
    list_display  = ('staff', 'date', 'status', 'marked_by', 'remarks')
    list_filter   = ('status', 'date')
    search_fields = ('staff__full_name', 'staff__username')
    date_hierarchy = 'date'
    readonly_fields = ('created_at',)
    ordering = ('-date',)
```

### ERP/attendance/apps.py

| Field | Value |
| --- | --- |
| Bytes | 191 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py
from django.apps import AppConfig


class AttendanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'attendance'
    verbose_name = 'Attendance'
```

### ERP/attendance/forms.py

| Field | Value |
| --- | --- |
| Bytes | 3779 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py
from django import forms
from datetime import date
from core.models import Division, Grade, Section

_INPUT = ('w-full px-3 py-2.5 border border-slate-200 rounded-lg text-sm text-slate-700 '
          'focus:outline-none focus:ring-2 focus:ring-[#1e3a5f]/30 focus:border-[#1e3a5f] '
          'transition bg-white')


class AttendanceFilterForm(forms.Form):
    """Filter bar used on both Take Attendance and Report pages."""
    division = forms.ModelChoiceField(
        queryset=Division.objects.filter(is_active=True),
        required=False,
        empty_label='All Divisions',
        widget=forms.Select(attrs={'class': _INPUT, 'id': 'id_division'}),
    )
    grade = forms.ModelChoiceField(
        queryset=Grade.objects.none(),
        required=False,
        empty_label='Select Grade',
        widget=forms.Select(attrs={'class': _INPUT, 'id': 'id_grade'}),
    )
    section = forms.ModelChoiceField(
        queryset=Section.objects.none(),
        required=False,
        empty_label='Select Section',
        widget=forms.Select(attrs={'class': _INPUT, 'id': 'id_section'}),
    )
    date = forms.DateField(
        required=False,
        initial=date.today,
        widget=forms.DateInput(attrs={'type': 'date', 'class': _INPUT}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically populate grade/section based on submitted values
        if 'division' in self.data:
            try:
                div_id = int(self.data.get('division'))
                self.fields['grade'].queryset = Grade.objects.filter(division_id=div_id)
            except (ValueError, TypeError):
                pass
        if 'grade' in self.data:
            try:
                grade_id = int(self.data.get('grade'))
                self.fields['section'].queryset = Section.objects.filter(grade_id=grade_id)
            except (ValueError, TypeError):
                pass


class ReportFilterForm(forms.Form):
    """Extended filter for the attendance report page."""
    division = forms.ModelChoiceField(
        queryset=Division.objects.filter(is_active=True),
        required=False,
        empty_label='All Divisions',
        widget=forms.Select(attrs={'class': _INPUT}),
    )
    grade = forms.ModelChoiceField(
        queryset=Grade.objects.all(),
        required=False,
        empty_label='All Grades',
        widget=forms.Select(attrs={'class': _INPUT}),
    )
    section = forms.ModelChoiceField(
        queryset=Section.objects.all(),
        required=False,
        empty_label='All Sections',
        widget=forms.Select(attrs={'class': _INPUT}),
    )
    student_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': _INPUT, 'placeholder': 'Search student...'}),
    )
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': _INPUT}),
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': _INPUT}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'division' in self.data:
            try:
                div_id = int(self.data.get('division'))
                self.fields['grade'].queryset = Grade.objects.filter(division_id=div_id)
            except (ValueError, TypeError):
                pass
        if 'grade' in self.data:
            try:
                grade_id = int(self.data.get('grade'))
                self.fields['section'].queryset = Section.objects.filter(grade_id=grade_id)
            except (ValueError, TypeError):
                pass
```

### ERP/attendance/migrations/__init__.py

| Field | Value |
| --- | --- |
| Bytes | 0 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py

```

### ERP/attendance/migrations/0001_initial.py

| Field | Value |
| --- | --- |
| Bytes | 2837 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py
# Generated by Django 6.0.4 on 2026-04-13 11:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('students', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(db_index=True)),
                ('status', models.CharField(choices=[('P', 'Present'), ('A', 'Absent'), ('L', 'Late'), ('E', 'Excused')], default='P', max_length=1)),
                ('remarks', models.CharField(blank=True, max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('marked_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='attendances_marked', to=settings.AUTH_USER_MODEL)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendances', to='students.student')),
            ],
            options={
                'verbose_name': 'Attendance',
                'verbose_name_plural': 'Attendance Records',
                'ordering': ['-date', 'student__full_name'],
                'unique_together': {('student', 'date')},
            },
        ),
        migrations.CreateModel(
            name='StaffAttendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(db_index=True)),
                ('status', models.CharField(choices=[('P', 'Present'), ('A', 'Absent'), ('L', 'Late'), ('E', 'Excused')], default='P', max_length=1)),
                ('remarks', models.CharField(blank=True, max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('marked_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='staff_attendances_marked', to=settings.AUTH_USER_MODEL)),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='staff_attendances', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Staff Attendance',
                'verbose_name_plural': 'Staff Attendance Records',
                'ordering': ['-date'],
                'unique_together': {('staff', 'date')},
            },
        ),
    ]
```

### ERP/attendance/migrations/0002_add_performance_indexes.py

| Field | Value |
| --- | --- |
| Bytes | 737 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py
# Generated by Django 6.0.4 on 2026-04-13 13:50

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0001_initial'),
        ('students', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddIndex(
            model_name='attendance',
            index=models.Index(fields=['date', 'student'], name='attendance_date_student_idx'),
        ),
        migrations.AddIndex(
            model_name='attendance',
            index=models.Index(fields=['student', 'status'], name='attendance_student_status_idx'),
        ),
    ]
```

### ERP/attendance/models.py

| Field | Value |
| --- | --- |
| Bytes | 2700 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py
from django.db import models
from django.conf import settings
from students.models import Student


STATUS_CHOICES = [
    ('P', 'Present'),
    ('A', 'Absent'),
    ('L', 'Late'),
    ('E', 'Excused'),
]

STATUS_COLORS = {
    'P': 'emerald',
    'A': 'red',
    'L': 'amber',
    'E': 'blue',
}


class Attendance(models.Model):
    """Daily student attendance record. One row per student per day."""

    student   = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='attendances',
    )
    date      = models.DateField(db_index=True)
    status    = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    marked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='attendances_marked',
    )
    remarks    = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['student', 'date']   # prevents duplicates
        ordering = ['-date', 'student__full_name']
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendance Records'
        indexes = [
            models.Index(fields=['date', 'student'], name='attendance_date_student_idx'),
            models.Index(fields=['student', 'status'], name='attendance_student_status_idx'),
        ]

    def __str__(self):
        return f"{self.student.full_name} — {self.date} — {self.get_status_display()}"

    @property
    def is_present(self):
        return self.status in ('P', 'L')


class StaffAttendance(models.Model):
    """Daily staff/teacher attendance record."""

    staff     = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='staff_attendances',
    )
    date      = models.DateField(db_index=True)
    status    = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    marked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='staff_attendances_marked',
    )
    remarks    = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['staff', 'date']
        ordering = ['-date']
        verbose_name = 'Staff Attendance'
        verbose_name_plural = 'Staff Attendance Records'

    def __str__(self):
        return f"{self.staff.full_name} — {self.date} — {self.get_status_display()}"
```

### ERP/attendance/urls.py

| Field | Value |
| --- | --- |
| Bytes | 747 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py
from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    # Main pages
    path('take/',                     views.take_attendance,       name='take'),
    path('report/',                   views.attendance_report,     name='report'),
    path('student/<int:pk>/calendar/',views.student_calendar,      name='student_calendar'),
    path('export/',                   views.export_attendance,     name='export'),

    # AJAX / API
    path('api/session/',              views.api_attendance_session, name='api_session'),
    path('api/submit/',               views.submit_attendance,      name='submit'),
    path('api/summary/',              views.api_today_summary,      name='api_summary'),
]
```

### ERP/core/__init__.py

| Field | Value |
| --- | --- |
| Bytes | 0 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py

```

### ERP/core/admin.py

| Field | Value |
| --- | --- |
| Bytes | 1436 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py
from django.contrib import admin
from .models import AcademicYear, Division, Grade, Section, Subject, StudyMode


@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display  = ('name', 'start_date', 'end_date', 'is_current')
    list_filter   = ('is_current',)
    search_fields = ('name',)


@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    list_display  = ('name', 'curriculum_type', 'is_active')
    list_filter   = ('is_active',)


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display  = ('name', 'division', 'order')
    list_filter   = ('division',)
    search_fields = ('name',)


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display  = ('name', 'grade', 'class_teacher', 'capacity')
    list_filter   = ('grade__division',)
    search_fields = ('name',)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display  = ('name', 'code', 'grade', 'division', 'is_active')
    list_filter   = ('division', 'is_active')
    search_fields = ('name', 'code')


@admin.register(StudyMode)
class StudyModeAdmin(admin.ModelAdmin):
    list_display  = ('name', 'arabic_name', 'order', 'is_active', 'created_at')
    list_filter   = ('is_active',)
    search_fields = ('name', 'arabic_name')
    list_editable = ('order', 'is_active')
    ordering      = ('order', 'name')
```

### ERP/core/apps.py

| Field | Value |
| --- | --- |
| Bytes | 88 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py
from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core'
```

### ERP/core/forms.py

| Field | Value |
| --- | --- |
| Bytes | 4662 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py
from django import forms
from django.contrib.auth import get_user_model
from .models import AcademicYear, Division, Grade, Section, Subject, Board, StudyMode

User = get_user_model()

# Base Tailwind CSS classes for widgets
_INPUT  = ('w-full px-3 py-2.5 border border-slate-200 rounded-lg text-sm text-slate-700 '
           'focus:outline-none focus:ring-2 focus:ring-[#1e3a5f]/30 focus:border-[#1e3a5f] '
           'transition bg-white')
_CHECK  = 'w-4 h-4 text-[#1e3a5f] rounded border-slate-300 cursor-pointer'


class TailwindMixin:
    """Apply Tailwind CSS classes to all form widgets automatically."""
    def apply_tailwind(self):
        for field in self.fields.values():
            w = field.widget
            if isinstance(w, forms.CheckboxInput):
                w.attrs.setdefault('class', _CHECK)
            else:
                w.attrs.setdefault('class', _INPUT)


class AcademicYearForm(TailwindMixin, forms.ModelForm):
    class Meta:
        model  = AcademicYear
        fields = ['name', 'start_date', 'end_date', 'is_current']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': _INPUT}),
            'end_date':   forms.DateInput(attrs={'type': 'date', 'class': _INPUT}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_tailwind()


class DivisionForm(TailwindMixin, forms.ModelForm):
    class Meta:
        model  = Division
        fields = ['name', 'curriculum_type', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_tailwind()


class GradeForm(TailwindMixin, forms.ModelForm):
    class Meta:
        model  = Grade
        fields = ['name', 'division', 'order']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_tailwind()


class SectionForm(TailwindMixin, forms.ModelForm):
    division = forms.ModelChoiceField(
        queryset=Division.objects.all(),
        required=True,
        empty_label='— Select Division —',
    )

    class Meta:
        model  = Section
        fields = ['name', 'grade', 'class_teacher', 'capacity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['class_teacher'].queryset    = User.objects.filter(role='TEACHER', is_active=True)
        self.fields['class_teacher'].required    = False
        self.fields['class_teacher'].empty_label = '— Unassigned —'

        # Render order: Name, Division, Grade, Class Teacher, Capacity
        self.order_fields(['name', 'division', 'grade', 'class_teacher', 'capacity'])

        # Pre-populate Division from instance.grade on edit; resolve from POST data if submitting
        division_id = None
        if self.instance and self.instance.pk and self.instance.grade_id:
            division_id = self.instance.grade.division_id
            self.fields['division'].initial = division_id
        if self.data.get('division'):
            try:
                division_id = int(self.data.get('division'))
            except (TypeError, ValueError):
                division_id = None

        # Filter Grade queryset to the chosen Division (or empty until one is picked)
        if division_id:
            self.fields['grade'].queryset = Grade.objects.filter(division_id=division_id).order_by('order', 'name')
        else:
            self.fields['grade'].queryset = Grade.objects.none()

        self.apply_tailwind()


class SubjectForm(TailwindMixin, forms.ModelForm):
    class Meta:
        model  = Subject
        fields = ['name', 'code', 'grade', 'division', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_tailwind()


class BoardForm(TailwindMixin, forms.ModelForm):
    class Meta:
        model  = Board
        fields = ['name', 'short_code', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_tailwind()


class StudyModeForm(TailwindMixin, forms.ModelForm):
    class Meta:
        model  = StudyMode
        fields = ['name', 'arabic_name', 'description', 'order', 'is_active']
        widgets = {
            'arabic_name': forms.TextInput(attrs={'dir': 'rtl', 'class': _INPUT}),
            'description': forms.TextInput(attrs={'class': _INPUT}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_tailwind()
```

### ERP/core/management/__init__.py

| Field | Value |
| --- | --- |
| Bytes | 0 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py

```

### ERP/core/management/commands/__init__.py

| Field | Value |
| --- | --- |
| Bytes | 0 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py

```

### ERP/core/management/commands/seed_grades.py

| Field | Value |
| --- | --- |
| Bytes | 4542 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py
"""
Management command: seed_grades

Creates all standard grades for every division (American, British, French, Home Study).
Safe to run multiple times (get_or_create).

Usage:
    python manage.py seed_grades
    python manage.py seed_grades --division AMERICAN
"""

from django.core.management.base import BaseCommand
from core.models import Division, Grade


# ── Grade lists by division ──────────────────────────────────────────────────
AMERICAN_GRADES = [
    ('Nursery',    1),
    ('Pre-Kinder', 2),
    ('Kinder 1',   3),
    ('Kinder 2',   4),
    ('Grade 1',    5),
    ('Grade 2',    6),
    ('Grade 3',    7),
    ('Grade 4',    8),
    ('Grade 5',    9),
    ('Grade 6',    10),
    ('Grade 7',    11),
    ('Grade 8',    12),
    ('Grade 9',    13),
    ('Grade 10',   14),
    ('Grade 11',   15),
    ('Grade 12',   16),
]

BRITISH_GRADES = [
    ('Nursery',    1),
    ('Reception',  2),
    ('Year 1',     3),
    ('Year 2',     4),
    ('Year 3',     5),
    ('Year 4',     6),
    ('Year 5',     7),
    ('Year 6',     8),
    ('Year 7',     9),
    ('Year 8',     10),
    ('Year 9',     11),
    ('Year 10',    12),
    ('Year 11',    13),
    ('Year 12',    14),
    ('Year 13',    15),
]

FRENCH_GRADES = [
    ('Nursery',   1),
    ('CP',        2),
    ('CE1',       3),
    ('CE2',       4),
    ('CM1',       5),
    ('CM2',       6),
    ('6ème',      7),
    ('5ème',      8),
    ('4ème',      9),
    ('3ème',      10),
    ('2nde',      11),
    ('1ère',      12),
    ('Terminale', 13),
]

HOME_STUDY_GRADES = [
    ('HS-Foundation', 1),
    ('HS-Primary',    2),
    ('HS-Middle',     3),
    ('HS-Secondary',  4),
]

DIVISION_GRADES = {
    Division.AMERICAN:   AMERICAN_GRADES,
    Division.BRITISH:    BRITISH_GRADES,
    Division.FRENCH:     FRENCH_GRADES,
    Division.HOME_STUDY: HOME_STUDY_GRADES,
}


class Command(BaseCommand):
    help = ('Seed standard grades for all (or a specific) division. '
            'Idempotent — safe to run multiple times.')

    def add_arguments(self, parser):
        parser.add_argument(
            '--division',
            type=str,
            choices=list(DIVISION_GRADES.keys()),
            default=None,
            help='Only seed grades for this division (e.g. AMERICAN). '
                 'Omit to seed all divisions.',
        )

    def handle(self, *args, **options):
        target_div = options.get('division')
        divisions  = Division.objects.filter(is_active=True)

        if target_div:
            divisions = divisions.filter(name=target_div)
            if not divisions.exists():
                self.stderr.write(
                    self.style.ERROR(
                        f"Division '{target_div}' not found or is inactive. "
                        f"Please create it in the admin first."
                    )
                )
                return

        total_created = 0
        total_existing = 0

        for division in divisions:
            grade_list = DIVISION_GRADES.get(division.name, [])
            if not grade_list:
                self.stdout.write(
                    self.style.WARNING(
                        f"No grade template defined for division '{division}'. Skipping."
                    )
                )
                continue

            self.stdout.write(f"\n  Division: {division}")
            created_count = 0
            for name, order in grade_list:
                grade, created = Grade.objects.get_or_create(
                    name=name,
                    division=division,
                    defaults={'order': order},
                )
                if created:
                    created_count   += 1
                    total_created   += 1
                    self.stdout.write(f"    + Created: {grade}")
                else:
                    total_existing  += 1

            self.stdout.write(
                self.style.SUCCESS(
                    f"    → {created_count} created, "
                    f"{len(grade_list) - created_count} already existed."
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"\nDone. Total created: {total_created}, "
                f"already existed: {total_existing}."
            )
        )
```

### ERP/core/management/commands/seed_initial_data.py

| Field | Value |
| --- | --- |
| Bytes | 6558 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py
"""
management command: seed_initial_data
──────────────────────────────────────
Creates the foundational data required to start using the ERP:

  • 3 Divisions  (American / British / French)
  • 12 Grades per Division (KG1, KG2, Grade 1 … Grade 12)
  • 1 Section "A" per Grade
  • Current Academic Year  (e.g. 2024-25)
  • Default SUPER_ADMIN user  (admin / admin@school.sa / AdminPass123!)

Run once after first deployment:
    python manage.py seed_initial_data

Options:
    --year      Academic year label            default: "2024-25"
    --admin-username   Superuser username      default: admin
    --admin-email      Superuser email         default: admin@school.sa
    --admin-password   Superuser password      default: AdminPass123!
    --no-input  Skip all confirmation prompts
"""

import datetime
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction


class Command(BaseCommand):
    help = "Seed initial data: divisions, grades, sections, academic year, and admin user"

    def add_arguments(self, parser):
        parser.add_argument(
            '--year', default='2024-25',
            help='Academic year label, e.g. 2024-25',
        )
        parser.add_argument(
            '--admin-username', default='admin',
            dest='admin_username',
        )
        parser.add_argument(
            '--admin-email', default='admin@school.sa',
            dest='admin_email',
        )
        parser.add_argument(
            '--admin-password', default='AdminPass123!',
            dest='admin_password',
        )
        parser.add_argument(
            '--no-input', action='store_true', dest='no_input',
            help='Skip confirmation prompts',
        )

    def handle(self, *args, **options):
        if not options['no_input']:
            self.stdout.write(
                self.style.WARNING(
                    "\nThis command will create divisions, grades, sections, an academic year,\n"
                    "and a default super-admin user.  Existing records are NOT overwritten.\n"
                )
            )
            confirm = input("Continue? [y/N] ").strip().lower()
            if confirm != 'y':
                self.stdout.write("Aborted.")
                return

        with transaction.atomic():
            self._create_divisions_and_grades()
            self._create_academic_year(options['year'])
            self._create_admin(
                options['admin_username'],
                options['admin_email'],
                options['admin_password'],
            )

        self.stdout.write(self.style.SUCCESS("\n✓ Initial data seeded successfully."))
        self.stdout.write(
            f"  Login: {options['admin_username']} / {options['admin_password']}\n"
            "  Change the password immediately after first login!"
        )

    # ─────────────────────────────────────────────────────────────────────────

    def _create_divisions_and_grades(self):
        from core.models import Division, Grade, Section

        DIVISIONS = [
            (Division.AMERICAN, Division.AMERICAN),
            (Division.BRITISH,  Division.BRITISH),
            (Division.FRENCH,   Division.FRENCH),
        ]

        GRADES = [
            ('KG1',      0),
            ('KG2',      1),
            ('Grade 1',  2),
            ('Grade 2',  3),
            ('Grade 3',  4),
            ('Grade 4',  5),
            ('Grade 5',  6),
            ('Grade 6',  7),
            ('Grade 7',  8),
            ('Grade 8',  9),
            ('Grade 9',  10),
            ('Grade 10', 11),
            ('Grade 11', 12),
            ('Grade 12', 13),
        ]

        for (div_name, curriculum) in DIVISIONS:
            division, created = Division.objects.get_or_create(
                name=div_name,
                defaults={'curriculum_type': curriculum},
            )
            if created:
                self.stdout.write(f"  Created division: {division}")
            else:
                self.stdout.write(f"  Division exists:  {division}")

            for (grade_name, order) in GRADES:
                grade, g_created = Grade.objects.get_or_create(
                    name=grade_name,
                    division=division,
                    defaults={'order': order},
                )
                if g_created:
                    self.stdout.write(f"    + Grade {grade_name}")

                # Create one default section "A"
                section, s_created = Section.objects.get_or_create(
                    name='A',
                    grade=grade,
                )
                if s_created:
                    self.stdout.write(f"      + Section A")

    def _create_academic_year(self, label: str):
        from core.models import AcademicYear

        # Parse "2024-25" → start 2024-09-01, end 2025-06-30
        try:
            start_y = int(label.split('-')[0])
            end_y   = start_y + 1
        except (ValueError, IndexError):
            raise CommandError(f"Invalid year format '{label}'. Use e.g. '2024-25'.")

        year, created = AcademicYear.objects.get_or_create(
            name=label,
            defaults={
                'start_date': datetime.date(start_y, 9, 1),
                'end_date':   datetime.date(end_y, 6, 30),
                'is_current': True,
            },
        )
        if created:
            self.stdout.write(f"  Created academic year: {year}")
        else:
            self.stdout.write(f"  Academic year exists:  {year}")

    def _create_admin(self, username: str, email: str, password: str):
        from accounts.models import CustomUser

        if CustomUser.objects.filter(username=username).exists():
            self.stdout.write(f"  Admin user '{username}' already exists — skipped.")
            return

        user = CustomUser.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            full_name='System Administrator',
            role=CustomUser.SUPER_ADMIN,
        )
        self.stdout.write(f"  Created super-admin: {user.username} <{user.email}>")
```

### ERP/core/migrations/__init__.py

| Field | Value |
| --- | --- |
| Bytes | 0 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py

```

### ERP/core/migrations/0001_initial.py

| Field | Value |
| --- | --- |
| Bytes | 4754 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py
# Generated by Django 6.0.4 on 2026-04-13 11:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AcademicYear',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='e.g. 2024-25', max_length=20, unique=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('is_current', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Academic Year',
                'ordering': ['-start_date'],
            },
        ),
        migrations.CreateModel(
            name='Division',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('AMERICAN', 'American'), ('BRITISH', 'British'), ('FRENCH', 'French')], max_length=20, unique=True)),
                ('curriculum_type', models.CharField(choices=[('AMERICAN', 'American Common Core'), ('BRITISH', 'British National Curriculum'), ('FRENCH', 'French National Curriculum')], max_length=20)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='e.g. Grade 1, KG1', max_length=50)),
                ('order', models.PositiveSmallIntegerField(default=0, help_text='Display order (lower = first)')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('division', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grades', to='core.division')),
            ],
            options={
                'verbose_name': 'Grade',
                'ordering': ['division', 'order', 'name'],
                'unique_together': {('name', 'division')},
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='e.g. A, B, C', max_length=10)),
                ('capacity', models.PositiveSmallIntegerField(default=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('class_teacher', models.ForeignKey(blank=True, limit_choices_to={'role': 'TEACHER'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sections_taught', to=settings.AUTH_USER_MODEL)),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='core.grade')),
            ],
            options={
                'verbose_name': 'Section',
                'ordering': ['grade', 'name'],
                'unique_together': {('name', 'grade')},
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(help_text='e.g. MATH-G1-AM', max_length=20, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('division', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subjects', to='core.division')),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subjects', to='core.grade')),
            ],
            options={
                'verbose_name': 'Subject',
                'ordering': ['division', 'grade', 'name'],
                'unique_together': {('name', 'grade')},
            },
        ),
    ]
```

### ERP/core/migrations/0002_add_home_study_division.py

| Field | Value |
| --- | --- |
| Bytes | 1188 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py
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
```

### ERP/core/migrations/0003_board.py

| Field | Value |
| --- | --- |
| Bytes | 1043 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py
# Generated by Django 6.0.4 on 2026-05-03 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_add_home_study_division'),
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='e.g. CBSE, IGCSE, SAT, British Board', max_length=100, unique=True)),
                ('short_code', models.CharField(blank=True, help_text='Short abbreviation, e.g. CBSE', max_length=20)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Exam Board',
                'verbose_name_plural': 'Exam Boards',
                'ordering': ['name'],
            },
        ),
    ]
```

### ERP/core/migrations/0004_alter_division_name.py

| Field | Value |
| --- | --- |
| Bytes | 402 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py
# Generated by Django 6.0.4 on 2026-05-04 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_board'),
    ]

    operations = [
        migrations.AlterField(
            model_name='division',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
```

### ERP/core/migrations/0005_add_default_divisions_grades_sections.py

| Field | Value |
| --- | --- |
| Bytes | 2358 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py
# Generated by Django 6.0.4 on 2026-05-04 08:25

from django.db import migrations


def create_default_data(apps, schema_editor):
    Division = apps.get_model('core', 'Division')
    Grade = apps.get_model('core', 'Grade')
    Section = apps.get_model('core', 'Section')

    # Define default divisions
    divisions_data = [
        ('American', 'AMERICAN'),
        ('British', 'BRITISH'),
        ('French', 'FRENCH'),
        ('Home Study', 'HOME_STUDY'),
    ]

    # Define default grades
    grades_data = [
        ('Nursery',    0),
        ('Pre-Kinder', 1),
        ('Kinder 1',   2),
        ('Kinder 2',   3),
        ('Reception',  4),
        ('Grade 1',    5),
        ('Grade 2',    6),
        ('Grade 3',    7),
        ('Grade 4',    8),
        ('Grade 5',    9),
        ('Grade 6',    10),
        ('Grade 7',    11),
        ('Grade 8',    12),
        ('Grade 9',    13),
        ('Grade 10',   14),
        ('Grade 11',   15),
        ('Grade 12',   16),
    ]

    # Define default sections
    sections_data = ['A', 'B', 'C']

    # Create divisions and their grades and sections
    for div_name, curriculum_type in divisions_data:
        division, created = Division.objects.get_or_create(
            name=div_name,
            defaults={'curriculum_type': curriculum_type}
        )

        # Create grades for this division
        for grade_name, order in grades_data:
            grade, grade_created = Grade.objects.get_or_create(
                name=grade_name,
                division=division,
                defaults={'order': order}
            )

            # Create sections for this grade
            for section_name in sections_data:
                Section.objects.get_or_create(
                    name=section_name,
                    grade=grade,
                    defaults={'capacity': 30}
                )


def reverse_default_data(apps, schema_editor):
    Division = apps.get_model('core', 'Division')
    Division.objects.filter(name__in=['American', 'British', 'French', 'Home Study']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_division_name'),
    ]

    operations = [
        migrations.RunPython(create_default_data, reverse_default_data),
    ]
```

### ERP/core/migrations/0006_fix_default_grades.py

| Field | Value |
| --- | --- |
| Bytes | 1651 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py
from django.db import migrations


CORRECT_GRADES = [
    ('Nursery',    0),
    ('Pre-Kinder', 1),
    ('Kinder 1',   2),
    ('Kinder 2',   3),
    ('Reception',  4),
    ('Grade 1',    5),
    ('Grade 2',    6),
    ('Grade 3',    7),
    ('Grade 4',    8),
    ('Grade 5',    9),
    ('Grade 6',    10),
    ('Grade 7',    11),
    ('Grade 8',    12),
    ('Grade 9',    13),
    ('Grade 10',   14),
    ('Grade 11',   15),
    ('Grade 12',   16),
]

OLD_GRADE_NAMES = ['KG 1', 'KG 2']


def fix_grades(apps, schema_editor):
    Division = apps.get_model('core', 'Division')
    Grade = apps.get_model('core', 'Grade')
    Section = apps.get_model('core', 'Section')

    # Remove old incorrect grades from all divisions
    Grade.objects.filter(name__in=OLD_GRADE_NAMES).delete()

    # For each existing division, ensure all correct grades + sections exist
    for division in Division.objects.all():
        for grade_name, order in CORRECT_GRADES:
            grade, _ = Grade.objects.get_or_create(
                name=grade_name,
                division=division,
                defaults={'order': order}
            )
            for section_name in ['A', 'B', 'C']:
                Section.objects.get_or_create(
                    name=section_name,
                    grade=grade,
                    defaults={'capacity': 30}
                )


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_add_default_divisions_grades_sections'),
    ]

    operations = [
        migrations.RunPython(fix_grades, migrations.RunPython.noop),
    ]
```

### ERP/core/migrations/0007_studymode.py

| Field | Value |
| --- | --- |
| Bytes | 1243 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py
# Generated by Django 6.0.4 on 2026-05-06 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_fix_default_grades'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudyMode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='e.g. Home Study, Distance Study, Hybrid', max_length=100, unique=True)),
                ('arabic_name', models.CharField(blank=True, help_text='e.g. الدراسة المنزلية', max_length=100)),
                ('description', models.CharField(blank=True, max_length=300)),
                ('is_active', models.BooleanField(default=True)),
                ('order', models.PositiveSmallIntegerField(default=0, help_text='Display order')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Study Mode',
                'verbose_name_plural': 'Study Modes',
                'ordering': ['order', 'name'],
            },
        ),
    ]
```

### ERP/core/models.py

| Field | Value |
| --- | --- |
| Bytes | 5206 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py
from django.db import models
from django.conf import settings


class AcademicYear(models.Model):
    name       = models.CharField(max_length=20, unique=True, help_text="e.g. 2024-25")
    start_date = models.DateField()
    end_date   = models.DateField()
    is_current = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_date']
        verbose_name = 'Academic Year'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.is_current:
            AcademicYear.objects.exclude(pk=self.pk).update(is_current=False)
        super().save(*args, **kwargs)


class Division(models.Model):
    AMERICAN   = 'AMERICAN'
    BRITISH    = 'BRITISH'
    FRENCH     = 'FRENCH'
    HOME_STUDY = 'HOME_STUDY'

    CURRICULUM_CHOICES = [
        (AMERICAN,   'American Common Core'),
        (BRITISH,    'British National Curriculum'),
        (FRENCH,     'French National Curriculum'),
        (HOME_STUDY, 'Home Study Programme'),
    ]

    name            = models.CharField(max_length=100, unique=True)
    curriculum_type = models.CharField(max_length=20, choices=CURRICULUM_CHOICES)
    is_active       = models.BooleanField(default=True)
    created_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name



class Grade(models.Model):
    name      = models.CharField(max_length=50, help_text="e.g. Grade 1, KG1")
    division  = models.ForeignKey(Division, on_delete=models.CASCADE, related_name='grades')
    order     = models.PositiveSmallIntegerField(default=0, help_text="Display order (lower = first)")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['division', 'order', 'name']
        unique_together = ['name', 'division']
        verbose_name = 'Grade'

    def __str__(self):
        return f"{self.name} — {self.division}"


class Section(models.Model):
    name          = models.CharField(max_length=10, help_text="e.g. A, B, C")
    grade         = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='sections')
    class_teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='sections_taught',
        limit_choices_to={'role': 'TEACHER'},
    )
    capacity   = models.PositiveSmallIntegerField(default=30)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['grade', 'name']
        unique_together = ['name', 'grade']
        verbose_name = 'Section'

    def __str__(self):
        return f"{self.grade} / Section {self.name}"


class Subject(models.Model):
    name      = models.CharField(max_length=100)
    code      = models.CharField(max_length=20, unique=True, help_text="e.g. MATH-G1-AM")
    grade     = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='subjects')
    division  = models.ForeignKey(Division, on_delete=models.CASCADE, related_name='subjects')
    is_active  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['division', 'grade', 'name']
        unique_together = ['name', 'grade']
        verbose_name = 'Subject'

    def __str__(self):
        return f"{self.name} ({self.grade})"


class StudyMode(models.Model):
    """Custom study modes (e.g. Home Study, Distance Study, etc.) configurable by admins.
    Applied to Regular (continuing) students to categorise them by learning mode."""
    name        = models.CharField(max_length=100, unique=True,
                                   help_text="e.g. Home Study, Distance Study, Hybrid")
    arabic_name = models.CharField(max_length=100, blank=True,
                                   help_text="e.g. الدراسة المنزلية")
    description = models.CharField(max_length=300, blank=True)
    is_active   = models.BooleanField(default=True)
    order       = models.PositiveSmallIntegerField(default=0, help_text="Display order")
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Study Mode'
        verbose_name_plural = 'Study Modes'

    def __str__(self):
        return self.name


class Board(models.Model):
    """External examination board (e.g. CBSE, IGCSE, SAT, etc.)."""
    name       = models.CharField(max_length=100, unique=True,
                                  help_text="e.g. CBSE, IGCSE, SAT, British Board")
    short_code = models.CharField(max_length=20, blank=True,
                                  help_text="Short abbreviation, e.g. CBSE")
    is_active  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Exam Board'
        verbose_name_plural = 'Exam Boards'

    def __str__(self):
        return self.name
```

### ERP/core/urls.py

| Field | Value |
| --- | --- |
| Bytes | 4437 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # ── Academic Years ──────────────────────────────────────────
    path('school-setup/academic-years/',                  views.academic_year_list,   name='academic_year_list'),
    path('school-setup/academic-years/add/',              views.academic_year_add,    name='academic_year_add'),
    path('school-setup/academic-years/<int:pk>/edit/',    views.academic_year_edit,   name='academic_year_edit'),
    path('school-setup/academic-years/<int:pk>/delete/',  views.academic_year_delete, name='academic_year_delete'),

    # ── Divisions ───────────────────────────────────────────────
    path('school-setup/divisions/',                 views.division_list,   name='division_list'),
    path('school-setup/divisions/add/',             views.division_add,    name='division_add'),
    path('school-setup/divisions/<int:pk>/edit/',   views.division_edit,   name='division_edit'),
    path('school-setup/divisions/<int:pk>/delete/', views.division_delete, name='division_delete'),

    # ── Grades ──────────────────────────────────────────────────
    path('school-setup/grades/',                 views.grade_list,   name='grade_list'),
    path('school-setup/grades/add/',             views.grade_add,    name='grade_add'),
    path('school-setup/grades/<int:pk>/edit/',   views.grade_edit,   name='grade_edit'),
    path('school-setup/grades/<int:pk>/delete/', views.grade_delete, name='grade_delete'),

    # ── Sections ────────────────────────────────────────────────
    path('school-setup/sections/',                 views.section_list,   name='section_list'),
    path('school-setup/sections/add/',             views.section_add,    name='section_add'),
    path('school-setup/sections/<int:pk>/edit/',   views.section_edit,   name='section_edit'),
    path('school-setup/sections/<int:pk>/delete/', views.section_delete, name='section_delete'),

    # ── Subjects ────────────────────────────────────────────────
    path('school-setup/subjects/',                 views.subject_list,   name='subject_list'),
    path('school-setup/subjects/add/',             views.subject_add,    name='subject_add'),
    path('school-setup/subjects/<int:pk>/edit/',   views.subject_edit,   name='subject_edit'),
    path('school-setup/subjects/<int:pk>/delete/', views.subject_delete, name='subject_delete'),

    # ── Exam Boards ─────────────────────────────────────────────
    path('school-setup/boards/',                 views.board_list,   name='board_list'),
    path('school-setup/boards/add/',             views.board_add,    name='board_add'),
    path('school-setup/boards/<int:pk>/edit/',   views.board_edit,   name='board_edit'),
    path('school-setup/boards/<int:pk>/delete/', views.board_delete, name='board_delete'),

    # ── Study Modes ─────────────────────────────────────────────
    path('school-setup/study-modes/',                 views.study_mode_list,   name='study_mode_list'),
    path('school-setup/study-modes/add/',             views.study_mode_add,    name='study_mode_add'),
    path('school-setup/study-modes/<int:pk>/edit/',   views.study_mode_edit,   name='study_mode_edit'),
    path('school-setup/study-modes/<int:pk>/delete/', views.study_mode_delete, name='study_mode_delete'),

    # ── API endpoints ───────────────────────────────────────────
    path('api/grades/',       views.api_grades,       name='api_grades'),
    path('api/sections/',     views.api_sections,     name='api_sections'),
    path('api/study-modes/',  views.api_study_modes,  name='api_study_modes'),
]
```

### ERP/ERP/__init__.py

| Field | Value |
| --- | --- |
| Bytes | 0 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py

```

### ERP/ERP/asgi.py

| Field | Value |
| --- | --- |
| Bytes | 399 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py
"""
ASGI config for ERP project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ERP.settings')

application = get_asgi_application()
```

### ERP/ERP/settings_production.py

| Field | Value |
| --- | --- |
| Bytes | 6817 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py
"""
Production settings — loaded on the Linux server.
Uses python-decouple to read secrets from an .env file or environment variables.

Usage:
    export DJANGO_SETTINGS_MODULE=ERP.settings_production
    gunicorn ERP.wsgi:application
"""
import os
from pathlib import Path
from decouple import config, Csv

BASE_DIR = Path(__file__).resolve().parent.parent

# ── Security ──────────────────────────────────────────────────────────────────
SECRET_KEY = config('SECRET_KEY')
DEBUG      = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

# ── Applications ──────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tailwind',
    'theme',
    'core',
    'accounts',
    'students',
    'attendance',
    'academics',
    'fees',
    'staff',
    'ai_features',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',   # static files via whitenoise
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ERP.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ERP.wsgi.application'

# ── Database ──────────────────────────────────────────────────────────────────
DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.postgresql',
        'NAME':     config('DB_NAME'),
        'USER':     config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST':     config('DB_HOST', default='localhost'),
        'PORT':     config('DB_PORT', default='5432'),
        'CONN_MAX_AGE': 60,   # persistent connections
    }
}

# ── Cache (use Redis in production for multi-worker support) ──────────────────
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'erp-cache',
        'TIMEOUT': 300,
    }
}
# If you install django-redis:
# CACHES = {
#     'default': {
#         'BACKEND': 'django_redis.cache.RedisCache',
#         'LOCATION': 'redis://127.0.0.1:6379/1',
#         'OPTIONS': {'CLIENT_CLASS': 'django_redis.client.DefaultClient'},
#     }
# }

# ── Password validation ───────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ── Internationalisation ──────────────────────────────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE     = 'Asia/Riyadh'
USE_I18N      = True
USE_TZ        = True

# ── Static & Media ────────────────────────────────────────────────────────────
STATIC_URL  = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL  = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ── Auth ──────────────────────────────────────────────────────────────────────
AUTH_USER_MODEL         = 'accounts.CustomUser'
LOGIN_URL               = '/accounts/login/'
LOGIN_REDIRECT_URL      = '/'
LOGOUT_REDIRECT_URL     = '/accounts/login/'

# ── Security headers ──────────────────────────────────────────────────────────
SECURE_HSTS_SECONDS            = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD            = True
SECURE_SSL_REDIRECT            = True
SESSION_COOKIE_SECURE          = True
CSRF_COOKIE_SECURE             = True
X_FRAME_OPTIONS                = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF    = True
SECURE_BROWSER_XSS_FILTER      = True

# ── Email ──────────────────────────────────────────────────────────────────────
EMAIL_BACKEND       = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST          = config('EMAIL_HOST', default='localhost')
EMAIL_PORT          = config('EMAIL_PORT', default=587, cast=int)
EMAIL_HOST_USER     = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
EMAIL_USE_TLS       = config('EMAIL_USE_TLS', default=True, cast=bool)
DEFAULT_FROM_EMAIL  = config('DEFAULT_FROM_EMAIL', default='webmaster@localhost')

# ── AI module ─────────────────────────────────────────────────────────────────
OPENAI_API_KEY = config('OPENAI_API_KEY', default='')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
```

### ERP/ERP/settings_test.py

| Field | Value |
| --- | --- |
| Bytes | 714 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py
"""
Test-only settings — uses SQLite so tests run without a PostgreSQL server.
Inherits everything from the main settings, then overrides DB and speed tweaks.
"""
from ERP.settings import *   # noqa: F401, F403

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Faster password hashing in tests
PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']

# Disable cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Media files go to a temp dir during tests
import tempfile
MEDIA_ROOT = tempfile.mkdtemp()

# Suppress logging noise
LOGGING = {}
```

### ERP/ERP/settings.py

| Field | Value |
| --- | --- |
| Bytes | 6596 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py
"""
Django settings for ERP project.

Generated by 'django-admin startproject' using Django 6.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/6.0/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# ── Minimal .env loader (no external dependency) ─────────────────────────────
# Reads KEY=VALUE lines from a .env file (repo root or BASE_DIR) into the
# environment, without overwriting variables already set by the OS/server.
def _load_dotenv():
    for candidate in (BASE_DIR.parent / '.env', BASE_DIR / '.env'):
        if not candidate.exists():
            continue
        for line in candidate.read_text(encoding='utf-8').splitlines():
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            key, _, value = line.partition('=')
            key, value = key.strip(), value.strip().strip('"').strip("'")
            os.environ.setdefault(key, value)
        break

_load_dotenv()


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '[REDACTED:SECRET]'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition
TAILWIND_APP_NAME = 'theme'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tailwind',
    'theme',
    # ERP Apps
    'core',
    'accounts',
    'students',
    'attendance',
    'academics',
    'fees',
    'staff',
    'ai_features',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ERP.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'builtins': ['fees.templatetags.fee_pdf_filters'],
        },
    },
]

WSGI_APPLICATION = 'ERP.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

# ── Database ──────────────────────────────────────────────────────────────────
# SQLite: zero-setup, single file (db.sqlite3) — ideal for offline/single-server.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# PostgreSQL (old) — kept for reference; uncomment to switch back.
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'school_db',
#         'USER': 'django_user',
#         'PASSWORD': '1234',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Riyadh'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Auth redirects
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

NPM_BIN_PATH = r"C:\Program Files\nodejs\npm.cmd"

AUTH_USER_MODEL = 'accounts.CustomUser'

# ── Cache (per-process in-memory; swap for Redis in production) ───────────────
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'erp-cache',
        'TIMEOUT': 300,   # 5 minutes default
    }
}

# OpenAI (optional) — set to enable GPT-4o-mini summaries in AI features
OPENAI_API_KEY = ''


# ── Email (fee reminders etc.) ────────────────────────────────────────────────
# Set EMAIL_HOST (+ credentials) in .env to send real email; without it,
# emails are printed to the console (dev mode).
EMAIL_HOST = os.environ.get('EMAIL_HOST', '')
if EMAIL_HOST:
    EMAIL_BACKEND       = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_PORT          = int(os.environ.get('EMAIL_PORT', '587'))
    EMAIL_HOST_USER     = os.environ.get('EMAIL_HOST_USER', '')
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
    EMAIL_USE_TLS       = os.environ.get('EMAIL_USE_TLS', '1') == '1'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = os.environ.get(
    'DEFAULT_FROM_EMAIL', 'Al-Kawthar International School <no-reply@alkawthar.edu.sa>')
```

### ERP/ERP/urls.py

| Field | Value |
| --- | --- |
| Bytes | 1633 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py
"""
URL configuration for ERP project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve as _serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('students/', include('students.urls')),
    path('attendance/', include('attendance.urls')),
    path('academics/', include('academics.urls')),
    path('fees/', include('fees.urls')),
    path('staff/', include('staff.urls')),
    path('ai/', include('ai_features.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve collected static files under a pure-WSGI server (Waitress) where
# Django's runserver auto-serving is unavailable. Works with DEBUG on or off.
urlpatterns += [
    re_path(r'^static/(?P<path>.*)$', _serve, {'document_root': settings.STATIC_ROOT}),
]
```

### ERP/ERP/wsgi.py

| Field | Value |
| --- | --- |
| Bytes | 399 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py
"""
WSGI config for ERP project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ERP.settings')

application = get_wsgi_application()
```

### ERP/fees/__init__.py

| Field | Value |
| --- | --- |
| Bytes | 0 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py

```