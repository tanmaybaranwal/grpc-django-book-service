from grpc_book_service_backend.settings.base import *

THIRD_PARTY_APPS = []
APPS = [
    "grpc_book_service",
]

INSTALLED_APPS += THIRD_PARTY_APPS
INSTALLED_APPS += APPS

for app_name in APPS:
    try:
        _dict = {}
        locals().update(
            {name: _dict["module_dict"][name] for name in _dict["to_import"]})
    except ImportError, err:
        print err

SECRET_KEY = '^d*66-07r)+k7-sajdhakshdaksjhdkj+d7*xg&q!5gk#'

DEBUG = True

PRINT_REQUEST_RESPONSE_TO_CONSOLE = True

################# Databases ##################


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
import uuid

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'TEST': {
            'NAME': '/tmp/%s.sqlite3' % str(uuid.uuid4()),
            'ENGINE': 'django.db.backends.sqlite3'
        }
    }
}

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
