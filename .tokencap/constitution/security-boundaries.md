# Security Boundaries

> TokenCap Constitution Engine

## 🟠 CONST-SEC-4B0E09 — HIGH

**Security middleware (helmet, CORS, CSRF) must remain enabled.**

> **Why:** These middleware prevent common web security vulnerabilities (XSS, CSRF, clickjacking).

> **What breaks:** Applications become vulnerable to XSS, clickjacking, and CSRF attacks.

*Files:* `ERP/ERP/settings.py`, `ERP/ERP/settings_production.py`, `deploy/fix_static/settings.py`

## 🔴 CONST-SEC-A2EA57 — CRITICAL

**Environment variable files (.env) must never be committed to version control.**

> **Why:** .env files contain secrets. Committing them exposes credentials to all repository users.

> **What breaks:** All secrets in .env become public. Immediate security incident.

*Files:* `.env`, `.env.example`
