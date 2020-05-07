"""
WSGI config for blog_backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

conf_path = "blog_backend.settings"
if os.getenv("BLOGHOME"):
    conf_path += ".pro"
else:
    conf_path += ".dev"
os.environ.setdefault('DJANGO_SETTINGS_MODULE', conf_path)

application = get_wsgi_application()
