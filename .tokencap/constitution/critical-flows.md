# Critical Flows

> TokenCap Constitution Engine

## 🔴 CONST-FLOW-88E4F2 — CRITICAL

**Authentication Flow is repository-critical and must remain intact end-to-end.**

> **Why:** Every protected page and authenticated feature depends on this flow working correctly.

> **What breaks:** Users cannot log in. All authenticated features become unreachable. Sessions invalidated.

*Files:* `ERP/students/migrations/0009_add_authorized_pickup.py`, `ERP/tests/integration/test_auth.py`

## 🔴 CONST-FLOW-260936 — CRITICAL

**Payment Flow is repository-critical. Checkout must complete reliably.**

> **Why:** Revenue depends entirely on the payment flow being operational and correct.

> **What breaks:** Users cannot complete purchases. Revenue stops. Potential chargebacks and disputes.

*Files:* `ERP/fees/migrations/0006_payment_plan.py`, `ERP/fees/migrations/0012_payment_mode_credit_bank_installment.py`, `ERP/fees/migrations/0016_add_feetype_fixed_down_payment.py`, `ERP/fees/migrations/0017_add_feestructure_min_down_payment.py`, `ERP/fees/migrations/0035_payment_plan_semester.py`

## 🔴 CONST-FLOW-862097 — CRITICAL

**Notification Pipeline (email, webhook, SMS) must remain operational.**

> **Why:** Notifications are critical for transactional communication (receipts, alerts, order updates).

> **What breaks:** Users stop receiving transactional emails. Webhooks fail silently. Integrations break.

*Files:* `ERP/students/migrations/0016_student_fees_contact_email_and_more.py`
