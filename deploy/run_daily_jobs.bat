@echo off
REM ============================================================
REM  Al-Kawthar ERP — NIGHTLY JOBS (Task Scheduler runs this)
REM  backup -> fee statuses -> staff document alerts -> admin email
REM  Manually bhi chala sakte ho: double-click.
REM ============================================================
cd /d "%~dp0..\ERP"
set PYTHONUTF8=1
if not exist logs mkdir logs
echo. >> logs\daily_jobs.log
echo ===== %DATE% %TIME% ===== >> logs\daily_jobs.log
"..\venv\Scripts\python.exe" manage.py run_daily_jobs >> logs\daily_jobs.log 2>&1
exit /b %ERRORLEVEL%
