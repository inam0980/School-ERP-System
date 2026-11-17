@echo off
REM ============================================================
REM  Al-Kawthar ERP — INSTALL NIGHTLY JOBS (one time)
REM  RIGHT-CLICK this file  ->  "Run as administrator"
REM  Har raat 2:00 AM: backup + fee status update + staff
REM  document alerts + admins ko daily report email.
REM ============================================================
cd /d "%~dp0.."
set ROOT=%CD%

net session >nul 2>&1
if errorlevel 1 (
    echo.
    echo  !! Administrator ke roop me chalao !!
    echo  Is file par right-click -^> "Run as administrator"
    echo.
    pause
    exit /b 1
)

set TASK=AlKawtharERP-DailyJobs

echo === Scheduling nightly jobs (daily 02:00) ===
schtasks /create /tn "%TASK%" /tr "\"%ROOT%\deploy\run_daily_jobs.bat\"" /sc daily /st 02:00 /ru SYSTEM /rl HIGHEST /f
if errorlevel 1 (
    echo  !! Task create nahi hua. Upar ka error dekho.
    pause
    exit /b 1
)

echo === Running once now to test (backup is created) ===
call "%ROOT%\deploy\run_daily_jobs.bat"
if errorlevel 1 (
    echo  !! Test run me koi job FAIL hua — ERP\logs\daily_jobs.log dekho.
) else (
    echo  Test run OK.
)

echo.
echo ============================================================
echo  DONE!  Har raat 2:00 AM jobs chalenge.
echo  Backups:   ERP\backups   (ya .env me ERP_BACKUP_DIR=D:\ERP_Backups)
echo  Log:       ERP\logs\daily_jobs.log
echo  Hatana ho: schtasks /delete /tn "%TASK%" /f
echo  NOTE: Backup DOOSRI disk / Google Drive folder par rakho —
echo        same disk kharab hua to backup bhi jayega.
echo ============================================================
pause
