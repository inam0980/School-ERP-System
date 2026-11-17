# Architecture Laws

> TokenCap Constitution Engine

## 🟠 CONST-ARCH-BD3B55 — HIGH

**Services cannot import UI components.**

> **Why:** Importing UI components into services couples server-side logic to browser rendering. This breaks SSR, testability, and separation of concerns.

> **What breaks:** Server-side services gain browser-only dependencies. Unit tests for services fail. SSR breaks.

## 🟠 CONST-ARCH-C8FC0E — HIGH

**Controllers cannot access the database directly.**

> **Why:** Direct DB access in controllers bypasses the service layer. This breaks the layered architecture and makes logic untestable.

> **What breaks:** Business logic leaks into controllers. Database coupling makes refactoring expensive.

## 🟠 CONST-ARCH-AB5D67 — HIGH

**Route handlers cannot access the database directly.**

> **Why:** Routes should delegate to services/controllers, not query the database themselves.

> **What breaks:** Business logic scattered across route files. Impossible to test in isolation.

## 🟠 CONST-ARCH-5A618E — HIGH

**UI components cannot import server-only modules.**

> **Why:** Server-only modules may contain secrets or Node.js-only APIs that crash in the browser.

> **What breaks:** Build errors in browser environments. Potential secret exposure.

## 🟠 CONST-ARCH-BC117A — HIGH

**High-impact clusters (Academics (models), Other, Students (models)) must not gain new circular dependencies.**

> **Why:** High-impact clusters already coordinate many modules. Adding circular imports makes builds fragile.

> **What breaks:** Module resolution fails. Build tools (webpack, esbuild) may hang or produce incorrect output.
