"""
WSGI config for terraform_manager project.
It exposes the WSGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ictsc_prep_school.ictsc_prep_school.settings.terraform_manager.develop")

application = get_wsgi_application()
