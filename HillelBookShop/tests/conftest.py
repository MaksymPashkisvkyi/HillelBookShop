import pytest
from rest_framework.test import APIClient


@pytest.fixture(autouse=True)
def media_root(settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path / "test-media"
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
    return settings.MEDIA_ROOT


@pytest.fixture
def api_client():
    return APIClient()
