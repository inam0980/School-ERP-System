# Compliance Rules

> TokenCap Constitution Engine

## 🔴 CONST-COMP-1A246E — CRITICAL

**Payment processing (PCI-DSS) — all Stripe/payment code requires compliance review.**

> **Why:** PCI-DSS requires that all payment card data handling meets security standards. Any change to payment flows must be reviewed.

> **What breaks:** PCI compliance violation. Payment processor account suspension. Legal liability.

*Files:* `ERP/static/js/tailwind.js`, `deploy/fix_static/tailwind.js`

## 🔴 CONST-COMP-B625B2 — CRITICAL

**HIPAA compliance — protected health information (PHI) handling must remain compliant.**

> **Why:** HIPAA requires strict access control, audit logging, and encryption for all PHI. Removing protections is illegal.

> **What breaks:** HIPAA violation. Criminal liability. Patient data exposed.

*Files:* `ERP/core/management/commands/seed_demo_data.py`, `ERP/core/management/commands/seed_students.py`, `gen_students.py`

## 🔴 CONST-COMP-9F1C07 — CRITICAL

**Audit logging must always be written and never removed.**

> **Why:** Audit logs provide the immutable record required for compliance, forensic investigation, and regulatory review.

> **What breaks:** Compliance audit failures. Inability to investigate security incidents. Regulatory violations.

*Files:* `ERP/students/models.py`
