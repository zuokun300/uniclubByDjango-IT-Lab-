import os
import sys
from pathlib import Path

from django.core.asgi import get_asgi_application


BASE_DIR = Path(__file__).resolve().parent.parent
site_packages = BASE_DIR / ".venv" / "lib" / f"python{sys.version_info.major}.{sys.version_info.minor}" / "site-packages"
if site_packages.exists():
    sys.path.insert(0, str(site_packages))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "it_site.settings")

application = get_asgi_application()
