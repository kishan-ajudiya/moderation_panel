"""
WSGI config for moderation_panel project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

moderation_panel_env = os.environ.get("MODERATION_PANEL_ENV")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moderation_panel.settings')

application = get_wsgi_application()
