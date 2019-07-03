from ictsc_prep_school.settings.terraform_manager.base import *
import os


def get_env_variable(var_name, default=None):
    """Get the environment variable or raise exception."""
    try:
        return os.environ[var_name]
    except KeyError:
        if default is not None:
            return default
        else:
            error_msg = 'The environment variable {} was missing, abort...' \
                .format(var_name)
            raise EnvironmentError(error_msg)


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

DEBUG = True
