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
