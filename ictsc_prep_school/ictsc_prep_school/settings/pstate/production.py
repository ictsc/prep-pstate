from ictsc_prep_school.settings.pstate.base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pstate',
        'USER': 'pstate',
        'PASSWORD': '',
        'HOST': 'db.prep.icttoracon.net',
        'PORT': '5432',
    }
}

BROKER_URL = 'redis://redis.prep.icttoracon.net:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis.prep.icttoracon.net:6379/0'

CSRF_TRUSTED_ORIGINS = [
        ".prep.icttoracon.net",
]

DEBUG = False
