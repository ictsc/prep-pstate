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
            #   FIX ME  :   docker-composeやk8s manifestに書いてあるenvを環境変数にセットできるようにする.
            # raise EnvironmentError(error_msg)
            return ''
