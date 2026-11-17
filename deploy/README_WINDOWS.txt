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


============================================================
 NIGHTLY AUTOMATION  (backup + fee status + alerts + report)
============================================================
 Ek baar:  deploy\install_daily_jobs.bat  -> right-click -> Run as administrator
 Har raat 2:00 AM ye chalega (sab kuch isi server par, koi data bahar nahi jaata):
   1. Database + uploaded files ka BACKUP  (verify hota hai, last 30 rakhta hai)
   2. Due date nikal gayi fees ko OVERDUE mark karna
   3. Staff Iqama (90 din) / MOE license (60 din) expiry check
   4. Admins (Super Admin / Admin with email) ko daily report email
 Log:  ERP\logs\daily_jobs.log

 BACKUP KAHAN JAYE (.env me likho, DOOSRI disk best hai):
   ERP_BACKUP_DIR=D:\ERP_Backups
   ERP_BACKUP_KEEP=30
 Abhi turant backup:   venv\Scripts\python ERP\manage.py backup_db

 RESTORE (galti / crash ke baad):
   1. Service band karo:   nssm\nssm.exe stop AlKawtharERP
   2. venv\Scripts\python ERP\manage.py restore_db ERP\backups\erp-YYYYMMDD-HHMMSS.sqlite3 --yes
      (purana database apne aap db.before-restore-....sqlite3 me save hota hai)
   3. Service chalu karo:  nssm\nssm.exe start AlKawtharERP

 PARENT FEE REMINDERS: "Send reminders" button ek family ko 7 din me
 sirf ek baar email karta hai (double-click se spam nahi). Har hafte
 automatic reminders chahiye to .env me:  ERP_AUTO_FEE_REMINDERS=true
 (default OFF)
