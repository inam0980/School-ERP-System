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
