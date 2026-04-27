# gunicorn.conf.py  — Gunicorn configuration for production
# Place this at: /home/erp/school-erp/gunicorn.conf.py

import multiprocessing

# Binding
bind    = "unix:/run/gunicorn/school_erp.sock"
# bind  = "127.0.0.1:8000"    # alternative: TCP socket

# Workers – recommended: (2 × CPU cores) + 1
workers     = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
threads     = 1
timeout     = 120
keepalive   = 5

# Logging
accesslog   = "/var/log/gunicorn/school_erp_access.log"
errorlog    = "/var/log/gunicorn/school_erp_error.log"
loglevel    = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)sμs'

# Process naming
proc_name   = "school_erp"

# Security
limit_request_line        = 8190
limit_request_fields      = 200
limit_request_field_size  = 8190

# Command to recalculate student fees
# python manage.py recalc_student_fees

