DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'klpdise',
        'USER': 'klp',
        'PASSWORD': 'klp',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
