from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
<<<<<<< HEAD
=======

>>>>>>> e8972cb74228f0025e74b408502006ef45737c8c
SECRET_KEY = 'django-insecure-graphene-trace-demo-key'
DEBUG = True
ALLOWED_HOSTS = ['*']

<<<<<<< HEAD
=======

>>>>>>> e8972cb74228f0025e74b408502006ef45737c8c
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
<<<<<<< HEAD
=======

>>>>>>> e8972cb74228f0025e74b408502006ef45737c8c
    'users',
    'dashboard',
]

<<<<<<< HEAD
=======

>>>>>>> e8972cb74228f0025e74b408502006ef45737c8c
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

<<<<<<< HEAD
ROOT_URLCONF = 'graphene_trace.urls'

=======

ROOT_URLCONF = 'graphene_trace.urls'


>>>>>>> e8972cb74228f0025e74b408502006ef45737c8c
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

<<<<<<< HEAD
WSGI_APPLICATION = 'graphene_trace.wsgi.application'

=======

WSGI_APPLICATION = 'graphene_trace.wsgi.application'


>>>>>>> e8972cb74228f0025e74b408502006ef45737c8c
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

<<<<<<< HEAD
AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

=======

AUTH_PASSWORD_VALIDATORS = []


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'   # change to your timezone if needed
USE_I18N = True
USE_TZ = True


>>>>>>> e8972cb74228f0025e74b408502006ef45737c8c
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

<<<<<<< HEAD
=======
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


>>>>>>> e8972cb74228f0025e74b408502006ef45737c8c
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'users.User'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard:role_redirect'
LOGOUT_REDIRECT_URL = 'login'