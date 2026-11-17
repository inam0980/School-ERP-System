"""
Production-safety tests for settings and file serving.

The live Windows server (serve.py → waitress) runs ERP.settings directly,
so these defaults ARE the production configuration.
"""
import os
import subprocess
import sys
from pathlib import Path

import pytest
from django.conf import settings
from django.core.management.utils import get_random_secret_key

pytestmark = [pytest.mark.django_db, pytest.mark.regression]

ERP_DIR = Path(__file__).resolve().parents[2]
PUBLIC_KEY_PREFIX = 'django-insecure-evg('     # leaked in git history — must never be used


def _settings_value(expr, **env):
    """Import ERP.settings in a fresh interpreter with a controlled environment."""
    clean = {k: v for k, v in os.environ.items()
             if k not in ('DJANGO_DEBUG', 'SECRET_KEY', 'DJANGO_ALLOWED_HOSTS')}
    clean.update({'DJANGO_SETTINGS_MODULE': 'ERP.settings', 'ERP_NO_DOTENV': '1',
                  'SECRET_KEY': 'test-key-' + 'x' * 40, **env})
    out = subprocess.run(
        [sys.executable, '-c', f'import ERP.settings as s; print({expr})'],
        cwd=ERP_DIR, env=clean, capture_output=True, text=True, timeout=60)
    assert out.returncode == 0, out.stderr
    return out.stdout.strip()


# ── BUG-13  Production ran with DEBUG=True and a SECRET_KEY that is public on GitHub

class TestBug13ProductionSettings:
    def test_debug_is_off_unless_explicitly_enabled(self):
        assert _settings_value('s.DEBUG') == 'False'

    @pytest.mark.parametrize("val, expected", [('true', 'True'), ('1', 'True'), ('False', 'False'), ('no', 'False')])
    def test_debug_can_be_enabled_for_development(self, val, expected):
        assert _settings_value('s.DEBUG', DJANGO_DEBUG=val) == expected

    def test_secret_key_comes_from_environment(self):
        assert _settings_value('s.SECRET_KEY', SECRET_KEY='from-env-' + 'k' * 40) == 'from-env-' + 'k' * 40

    def test_secret_key_is_generated_and_persisted_when_not_configured(self, tmp_path, monkeypatch):
        from ERP import settings as erp_settings
        monkeypatch.delenv('SECRET_KEY', raising=False)
        key_file = tmp_path / '.secret_key'
        first = erp_settings._secret_key(key_file)
        assert len(first) >= 50 and not first.startswith(PUBLIC_KEY_PREFIX)
        assert key_file.read_text().strip() == first
        assert erp_settings._secret_key(key_file) == first      # stable across restarts

    def test_leaked_key_is_not_in_use(self):
        assert not settings.SECRET_KEY.startswith(PUBLIC_KEY_PREFIX)
        assert not _settings_value('s.SECRET_KEY').startswith(PUBLIC_KEY_PREFIX)

    def test_errors_are_logged_when_debug_is_off(self):
        """With DEBUG off Django logs request errors nowhere by default."""
        assert _settings_value("'django.request' in s.LOGGING['loggers']") == 'True'

    def test_deploy_patch_copy_matches_live_settings(self):
        """deploy/fix_static/apply_fix.bat copies these over the server's files."""
        repo = ERP_DIR.parent
        for live, patch in [('ERP/ERP/settings.py', 'deploy/fix_static/settings.py'),
                            ('ERP/ERP/urls.py', 'deploy/fix_static/urls.py')]:
            a = (repo / live).read_text(encoding='utf-8').replace('\r\n', '\n')
            b = (repo / patch).read_text(encoding='utf-8').replace('\r\n', '\n')
            assert a == b, f"{patch} is out of sync with {live}"


# ── BUG-14  Uploaded media (student photos, passports) served with DEBUG off… and to anyone

class TestBug14MediaServing:
    @pytest.fixture
    def media_file(self):
        p = Path(settings.MEDIA_ROOT) / 'students' / 'documents' / 'AKS-X' / 'passport.pdf'
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(b'%PDF-1.4 secret')
        return '/media/students/documents/AKS-X/passport.pdf'

    def test_staff_can_load_media_with_debug_off(self, login, admin, media_file):
        assert settings.DEBUG is False
        resp = login(admin).get(media_file)
        assert resp.status_code == 200
        assert b''.join(resp.streaming_content) == b'%PDF-1.4 secret'

    def test_anonymous_cannot_download_documents(self, client, media_file):
        resp = client.get(media_file)
        assert resp.status_code == 302 and '/accounts/login' in resp['Location']

    def test_parent_cannot_download_documents(self, login, parent, media_file):
        assert login(parent).get(media_file).status_code in (302, 403)

    def test_path_traversal_is_blocked(self, login, admin, media_file):
        for attempt in ('/media/../ERP/settings.py', '/media/..%2F..%2FERP%2Fsettings.py'):
            assert login(admin).get(attempt).status_code in (400, 404)
