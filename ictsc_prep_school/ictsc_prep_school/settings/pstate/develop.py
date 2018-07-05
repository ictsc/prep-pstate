from ictsc_prep_school.settings.pstate.base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'terraform_manager2',
        'USER': 'terraform',
        'PASSWORD': 'terraform',
        'HOST': '163.43.30.30',
        'PORT': '5432',
    }
}

BROKER_URL = 'redis://59.106.211.157:6379/0'
CELERY_RESULT_BACKEND = 'redis://59.106.211.157:6379/0'

CSRF_TRUSTED_ORIGINS = [
        ".prep-dev.icttoracon.net",
]

DEBUG = True
