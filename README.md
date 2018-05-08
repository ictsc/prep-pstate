# pstate
## Deployment
### 0. Preparation of MQ (Redis) and DB(postgres)
Please prepare MQ (Redis) and DB (postgres).

### 1. Configure settings.py and DB initialization
Please change the setting to your environment.

Please edit the following file.
```
ictsc_prep_school/ictsc_prep_school/settings/pstate/production.py
ictsc_prep_school/ictsc_prep_school/settings/terraform_manager/production.py
```

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'terraform_manager',
        'USER': '<DB_USERNAME>',
        'PASSWORD': '<DB_PASSWORD>',
        'HOST': '<YOUR_DB_SERVER_IP_ADDRESS>',
        'PORT': '<YOUR_DB_SERVER_PORT>',
    }
}

BROKER_URL = 'redis://<YOUR_REDIS_SERVER_IP_ADDRESS>:6379/0'
CELERY_RESULT_BACKEND = 'redis://<YOUR_REDIS_SERVER_IP_ADDRESS>:6379/0'
```


Initial data is put in DB.
```
python manage.py migrate
python manage.py createsuperuser
python manage.py loaddata fixtures/attribute.json
python manage.py loaddata fixtures/provider.json
```

### 2. (optional) Creating and starting an API container
Execute the following command in the project root directory.

Create
```
docker build -t terraform-manager-api  -f docker_build/terraform_manager_api/Dockerfile .
```

Run
```
docker run -p 8000:80 -it terraform-manager-api
```

### 3. Creating and starting a worker container
Execute the following command in the project root directory.

Create
```
docker build -t terraform-manager-worker  -f docker/worker/Dockerfile .
```

Run
```
docker run -it terraform-manager-worker
```

### 4. Creating and starting a pstate webui container
Execute the following command in the project root directory.

Create
```
sh docker_build.sh
```

Run
```
docker run -p 80:80 -it pstate_webui:20180410
```