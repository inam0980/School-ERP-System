"""
Test-only settings — uses SQLite so tests run without a PostgreSQL server.
Inherits everything from the main settings, then overrides DB and speed tweaks.
"""
from ERP.settings import *   # noqa: F401, F403

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Faster password hashing in tests
PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']

# Disable cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Media files go to a temp dir during tests
import tempfile
MEDIA_ROOT = tempfile.mkdtemp()

# Suppress logging noise
LOGGING = {}
