"""
WSGI config for portal project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portal.settings')
BASE_DIR = Path(__file__).resolve().parent.parent

application = get_wsgi_application()

application = WhiteNoise(application, root=os.path.join(BASE_DIR, 'staticfiles'))

application.add_files(os.path.join(BASE_DIR, 'media'), prefix='media/')