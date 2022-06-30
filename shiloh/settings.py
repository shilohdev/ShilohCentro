"""
Django settings for shiloh project.

Generated by 'django-admin startproject' using Django 3.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

# IMPORTAR O MÓDULO OS E PATH
# PATH -> MANIPULA O PATH
# OS -> SERVE PARA USAR AS FUNCIONALIDADES QUE DEPENDEM DO SISTEMA OPERACIONAL, COMO ARQUIVOS, ENVIRONMENT ETC.
from pathlib import Path
import os

# CRIAR ENVIRONMENT
# ENVIRONMENT -> SÃO VARIÁVEIS QUE FICAM MAIS FÁCEIS DE TROCAR

# DOMAIN PRINCIPAL -> AQUI USAREMOS PARA MONTAR AS URLS DE REDIRECIONAMENTO
os.environ['DOMAIN'] = 'shiloh.com.br'

# SECRET KEY -> PROTEGE O DJANGO
os.environ['SECRET_KEY'] = 'SE$cRET$dasi0ue0912ij3eioas09dufas90!@#!@$!@*#)(!@*)#(!@K'

# HOSTS PERMITIDOS PARA QUANDO FOREM ACESSAR O PROJETO - OS DOMINIOS // * -> ALL (RETIRAR NO PRODUÇÃO)
os.environ['DJANGO_ALLOWED_HOSTS'] = '127.0.0.1 *'

# DEBUG -> AQUI É PARA APARECER A TELA DE ERRO
# 1 -> SIM // NÃO RECOMENDÁVEL QUANDO PRODUÇÃO
# 0 -> NÃO
os.environ['DEBUG'] = '1'

# AMQP SETTINGS
# AMQP É O BANCO DE DADOS NA MEMÓRIA, NÃO SERVE PARA ARMAZENAMENTO COMO O MYSQL, MAS PARA CRIAR SOCKET, FILAS, CELERY, ETC, SERÁ USADO
# RABBITMQ -> SERÁ INSTALADO POR DOCKER
os.environ['AMQP_USER'] = 'guest'
os.environ['AMQP_PASSWORD'] = 'guest'
os.environ['AMQP_PORT'] = '5672'

# EMAIL SETTINGS
os.environ['EMAIL_HOST'] = 'mail.shiloh.com.br'
os.environ['EMAIL_PORT'] = '587'
os.environ['EMAIL_HOST_USER'] = 'informativo@shiloh.com.br'
os.environ['EMAIL_HOST_PASSWORD'] = 'guest'
os.environ['EMAIL_USE_TLS'] = '1'
os.environ['EMAIL_USE_SSL'] = '1'
os.environ['DEFAULT_FROM_EMAIL'] = 'informativo@shiloh.com.br'

# DATABASE SETTINGS
# DB ENVIRONMENT - PRD = PRODUÇÃO || HOM = HOMOLOGAÇÃO
os.environ['DATABASE_ENVIRONMENT'] = 'PRD'

# DB PRODUÇÃO
#os.environ['DATABASE_PRD_HOST'] = '34.94.95.255'
#os.environ['DATABASE_PRD_USER'] = 'root'
#os.environ['DATABASE_PRD_PASSWORD'] = '104da04a0895b21318d2b2d3600ce2c61231'
#os.environ['DATABASE_PRD_PORT'] = '3306'


# DB PRODUÇÃO
os.environ['DATABASE_PRD_HOST'] = '34.102.44.244'
os.environ['DATABASE_PRD_USER'] = 'root'
os.environ['DATABASE_PRD_PASSWORD'] = '104da04a0895b21318d2b2d3600ce2c61231'
os.environ['DATABASE_PRD_PORT'] = '3306'

# DB HOMOLOGAÇÃO
os.environ['DATABASE_HOM_HOST'] = 'localhost'
os.environ['DATABASE_HOM_USER'] = 'root'
os.environ['DATABASE_HOM_PASSWORD'] = 'my-secret-pw'
os.environ['DATABASE_HOM_PORT'] = '3306'


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", default="secret#$$!o1290ie09idasdm1p2k910ie0'1!@!O#_@#EWQ)")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.environ.get("DEBUG", default=0)))

#HOSTS
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")

#CSRF
CSRF_FAILURE_VIEW = 'initialize.views.csrf_failure'

#SETTINGS URLS
DOMAIN = os.environ.get("DOMAIN")
SHORT_URL = f"https://short.{DOMAIN}"

#AMQP
AMQP_USER = os.environ.get("AMQP_USER")
AMQP_PASSWORD = os.environ.get("AMQP_PASSWORD")
AMQP_PORT = os.environ.get("AMQP_PORT")

#CELERY
broker_url = f'amqp://{AMQP_USER}:{AMQP_PASSWORD}@localhost:{AMQP_PORT}//'
CELERY_BROKER_URL = f'amqp://{AMQP_USER}:{AMQP_PASSWORD}@localhost:{AMQP_PORT}//'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'America/Sao_Paulo'

#MAILER
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Host for sending e-mail.
EMAIL_HOST = os.environ.get("EMAIL_HOST")

# Port for sending e-mail.
EMAIL_PORT = os.environ.get("EMAIL_PORT")

# Optional SMTP authentication information for EMAIL_HOST.
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")

# Authentication
EMAIL_USE_TLS = bool(int(os.environ.get("EMAIL_USE_TLS", default=1)))
EMAIL_USE_SSL: bool(int(os.environ.get("EMAIL_USE_SSL", default=1)))

# DEFAULT FROM EMAIL
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL")

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'initialize',
    'auth_access',
    'auth_users',
    'functions',
    'auth_finances',
    'auth_permissions',
    'auth_dash',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

X_FRAME_OPTIONS = 'SAMEORIGIN'

ROOT_URLCONF = 'shiloh.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
            'libraries':{
                'functions': 'initialize.templatetags.functions',
            }
        },
    },
]

WSGI_APPLICATION = 'shiloh.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# PRD = PRODUÇÃO | HOM = HOMOLOGAÇÃO
DATABASE_ENVIRONMENT = os.environ.get("DATABASE_ENVIRONMENT")

# ACCOUNT
DATABASE_OPTIONS = {
    'ENGINE': 'mysql.connector.django',
    "PRD": {
        "host": os.environ.get("DATABASE_PRD_HOST", default=None),
        "user": os.environ.get("DATABASE_PRD_USER", default=None),
        "password": os.environ.get("DATABASE_PRD_PASSWORD", default=None),
        "port": os.environ.get("DATABASE_PRD_PORT", default=None)
    },
    "HOM": {
        "host": os.environ.get("DATABASE_HOM_HOST", default=None),
        "user": os.environ.get("DATABASE_HOM_USER", default=None),
        "password": os.environ.get("DATABASE_HOM_PASSWORD", default=None),
        "port": os.environ.get("DATABASE_HOM_PORT", default=None)
    },
    "DATABASES": {
        "auth_users": "auth_users",
        "userdb": "auth_users",
        "customer_refer": "customer_refer",
        "auth_permissions": "auth_permissions",
        "auth_agenda":"auth_agenda",
        "admins":"admins",
        "customer_refer":"customer_refer",
        "auth_finances":"auth_finances",
        
    }
}

DATABASE_HOST = DATABASE_OPTIONS[DATABASE_ENVIRONMENT]["host"]
DATABASE_USER = DATABASE_OPTIONS[DATABASE_ENVIRONMENT]["user"]
DATABASE_PASSWORD = DATABASE_OPTIONS[DATABASE_ENVIRONMENT]["password"]
DATABASE_PORT = DATABASE_OPTIONS[DATABASE_ENVIRONMENT]["port"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASE UPDATE
dkeys = DATABASE_OPTIONS["DATABASES"]
for k in dkeys:
    DATABASES.update({
        k: {
            'ENGINE': DATABASE_OPTIONS["ENGINE"],
            'NAME': dkeys[k],
            'USER': DATABASE_USER,
            'PASSWORD': DATABASE_PASSWORD,
            'HOST': DATABASE_HOST,
            'PORT': DATABASE_PORT,
        }
    })

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]

# Password hashers
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_L10N = True
USE_TZ = False

# SECURE
#SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'http')

SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = False
SECURE_SSL_REDIRECT = False

#POST

DATA_UPLOAD_MAX_MEMORY_SIZE = 52428800000
DATA_UPLOAD_MAX_NUMBER_FIELDS = 5000000000

CACHE_BACKEND = 'memcached://127.0.0.1:11211/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/app-assets/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

MEDIA_ROOT = os.path.join(BASE_DIR, 'docs/')

MEDIA_URL = "/docs/"

LOGIN_REDIRECT_URL = '/'

LOGOUT_REDIRECT_URL = '/accounts/login'

ASGI_APPLICATION = "initialize.asgi.application"

# BASE DOCS
BASE_DIR_DOCS = str(BASE_DIR).replace("\\", "/") + "/docs"
#SHORT_PLATAFORM = "http://127.0.0.1:8000"
SHORT_PLATAFORM = "https://shilohcentro.com.br" 
LISTPATHTYPE = {
    "1": "Comprovante de Pagamento",
    "2": "Nota Fiscal",
    "3": "Guia Médica",
    "4": "Outros",
    "5": "Carterinha Convênio",
    "6": "Documento Pessoal",
}

LISTPATHTYPEFINANCE = {
    "NF": "NF",
}