import os
from devtrac.settings import *  # noqa

os.environ.setdefault('DB_NAME', 'REPLACE_DB_NAME')
os.environ.setdefault('DB_USER', 'REPLACE_DB_USER')
os.environ.setdefault('DB_PASSWORD', 'REPLACE_DB_PASSWORD')
os.environ.setdefault('DB_HOST', 'REPLACE_DB_HOST')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME'),
        'USER':  os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST')
    }
}

DRUPAL_USERNAME = 'REPLACE_DRUPAL_USERNAME'
DRUPAL_PASSWORD = 'REPLACE_DRUPAL_PASSWORD'
TEST_FIELD_TRIP = u'A Demo Field Trip (15074)'
