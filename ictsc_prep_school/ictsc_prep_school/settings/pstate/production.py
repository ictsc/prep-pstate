from ictsc_prep_school.settings import get_env_variable
from ictsc_prep_school.settings.pstate.base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '{}'.format(get_env_variable('POSTGRES_DB')),
        'USER': '{}'.format(get_env_variable('POSTGRES_USER')),
        'PASSWORD': '{}'.format(get_env_variable('POSTGRES_PASSWORD')),
        'HOST': '{}'.format(get_env_variable('POSTGRES_HOST')),
        'PORT': '{}'.format(get_env_variable('POSTGRES_PORT')),
    }
}

BROKER_URL = 'redis://{}:{}/0'.format(get_env_variable('REDIS_HOST'), get_env_variable('REDIS_PORT'))
CELERY_RESULT_BACKEND = 'redis://{}:{}/0'.format(get_env_variable('REDIS_HOST'), get_env_variable('REDIS_PORT'))

CSRF_TRUSTED_ORIGINS = [
        ".{}".format(get_env_variable('CSRF_TRUSTED_ORIGIN')),
]

DEBUG = False
