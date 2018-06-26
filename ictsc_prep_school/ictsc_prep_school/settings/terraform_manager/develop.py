from ictsc_prep_school.settings.terraform_manager.base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'terraform_manager2',
        'USER': 'terraform',
        'PASSWORD': '',
        'HOST': 'db.prep-dev.icttoracon.net',
        'PORT': '5432',
    }
}

BROKER_URL = 'redis://59.106.211.157:6379/0'
CELERY_RESULT_BACKEND = 'redis://59.106.211.157:6379/0'

DEBUG = True
