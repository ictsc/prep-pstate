from ictsc_prep_school.settings import get_env_variable
from ictsc_prep_school.settings.terraform_manager.base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '{}'.format(get_env_variable('POSTGRES_DB')),
        'USER': '{}'.format(get_env_variable('POSTGRES_USER')),
        'PASSWORD': '{}'.format(get_env_variable('POSTGRES_PASSWORD')),
        'HOST': 'db.prep.icttoracon.net',
        'PORT': '5432',
    }
}

BROKER_URL = 'redis://redis.prep.icttoracon.net:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis.prep.icttoracon.net:6379/0'

DEBUG = False
