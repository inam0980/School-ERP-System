# Testing & TDD Guide

Every change to this ERP is test-driven. This file is the contract.

## Run the tests

From the `ERP/` folder, using the project venv:

```bash
../venv/Scripts/python -m pytest                 # everything (~20 s)
../venv/Scripts/python -m pytest -m unit         # fast, isolated tests only
../venv/Scripts/python -m pytest -m integration  # views, URLs, workflows
../venv/Scripts/python -m pytest -m regression   # bugs that must never return
../venv/Scripts/python -m pytest -k refund       # anything matching "refund"
../venv/Scripts/python -m pytest --cov=. --cov-report=html   # coverage → htmlcov/index.html
```

Tests use an in-memory SQLite DB (`ERP/settings_test.py`). They never touch the real database.

## Layout

| Folder | What goes here | Marker |
|---|---|---|
| `tests/unit/` | One model, form, helper or decorator. No HTTP. | `unit` (auto) |
| `tests/integration/` | Requests through the Django test client: pages, permissions, full workflows. | `integration` (auto) |
| `tests/integration/test_regressions.py` | One test per bug found. **Never delete.** | `regression` |
| `tests/integration/test_url_sweep.py` | Opens every URL as every role: no 500s, no GET side-effects, no permission leaks. | — |
| `tests/factories.py` | `factory_boy` factories: build test data here, not with raw `objects.create`. | — |
| `tests/conftest.py` | Shared fixtures: `admin`, `teacher`, `accountant`, `staff_user`, `parent`, `login`, `school`. | — |

## The TDD loop (mandatory)

1. **Red.** Write a test that describes the behaviour you want, or reproduces the bug. Run it and **watch it fail** for the right reason.
2. **Green.** Write the smallest code change that makes it pass.
3. **Refactor.** Clean up with the suite green. Run the full suite before pushing.

### For a bug

- Add a class to `test_regressions.py` named `TestBugNN<ShortName>`, with a comment describing the bug.
- Commit the test and the fix together. The message says what broke and why.

### For a new feature

- Model logic, calculations, validation → unit test first.
- New page or endpoint → integration test first: who can access it (one allowed role, one denied role), the happy path, one invalid input.
- **New URL with a `<pk>`** → add it to `ROUTE_OBJECTS` in `test_url_sweep.py`. The sweep fails until you do.
- **New URL readable by PARENT** → add it to `PUBLIC_TO_LOGGED_IN` *with a written reason*.

## Rules that keep the suite trustworthy

- **Money is `Decimal`.** Assert exact amounts (`D('1150.00')`), never floats.
- **Dates are relative.** Use `date.today() ± timedelta`, never hardcoded dates that silently become "the past" (this already broke the old suite once).
- **Every permission check gets a denial test.** "Admin can" is half a test. "Teacher cannot" is the other half.
- **A GET must never change data.** The URL sweep enforces this for every route.
- **Don't weaken a test to make it pass.** If a test pins behaviour that is a business decision (e.g. the grade-rounding policy in `test_models_misc.py`), change it only after the school confirms.

## Coverage ratchet

Current baseline: **66 %** (migrations, settings, seed scripts excluded via `.coveragerc`).
The pre-push hook fails if coverage drops below the number in `.githooks/pre-push`.
When coverage goes up, raise that number. It only ever goes up.

Enable the hook once per clone:

```bash
git config core.hooksPath .githooks
```
