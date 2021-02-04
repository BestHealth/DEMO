import os
from pathlib import Path
import djcelery
from django.core.wsgi import get_wsgi_application


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = '(drs1ja8bi3#79az(t6fl13&1hmwqmbn3=%7z%ln!_4$fwd1x*'

DEBUG = False

ALLOWED_HOSTS = ['*']


INVALID_TIME = 60 * 60 * 24

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'testing_user',
    'testing_runner',
    'rest_framework',
    'corsheaders',
    'djcelery',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'TestingRunner.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR.joinpath('templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'TestingRunner.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'NAME',
        'USER': 'USER',
        'PASSWORD': 'PASSWORD',
        'HOST': 'HOST',
        'PORT': 'PORT',
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


STATIC_URL = '/static/'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ['TestingRunner.auth.Authenticator'],
    'UNAUTHENTICATED_USER': None,
    'UNAUTHENTICATED_TOKEN': None,
    # 关闭rest_framework前端API模板
    'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer',),
    # json form 渲染
    'DEFAULT_PARSER_CLASSES': ['rest_framework.parsers.JSONParser',
                               'rest_framework.parsers.FormParser',
                               'rest_framework.parsers.MultiPartParser',
                               'rest_framework.parsers.FileUploadParser',
                               ],
    # 节流限制
    'DEFAULT_THROTTLE_CLASSES': [
        'TestingRunner.throttle.VisitThrottle',
        'TestingRunner.throttle.UserThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'Vistor': '300/m',
        'User': '300/m'
    },
    'DEFAULT_PAGINATION_CLASS': 'TestingRunner.pagination.MyPageNumberPagination',
}

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = ()

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)

CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
)

djcelery.setup_loader()
CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = 'Asia/Shanghai'
BROKER_URL = 'amqp://admin:admin@IP:端口/??'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERY_TASK_RESULT_EXPIRES = 7200
CELERYD_CONCURRENCY = 1 if DEBUG else 5
CELERYD_MAX_TASKS_PER_CHILD = 40

# 邮件配置
EMAIL_SERVER = '服务'
EMAIL_USERNAME = '邮件账号'
EMAIL_PASSWORD = '邮件授权码'
EMAIL_SENDER = '发送人'
# 报告URL，即后台部署URL
REPORT_URL = 'URL'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] - %(message)s'}
        # 日志格式
    },
    'filters': {
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR.joinpath('logs/debug.log'),
            'maxBytes': 1024 * 1024 * 50,
            'backupCount': 5,
            'formatter': 'standard',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'request_handler': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR.joinpath('logs/run.log'),
            'maxBytes': 1024 * 1024 * 50,
            'backupCount': 5,
            'formatter': 'standard',
        },
        'scprits_handler': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR.joinpath('logs/run.log'),
            'maxBytes': 1024 * 1024 * 100,
            'backupCount': 5,
            'formatter': 'standard',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['default', 'console'],
            'level': 'INFO',
            'propagate': True
        },
        'TestingRunner.app': {
            'handlers': ['default', 'console'],
            'level': 'INFO',
            'propagate': True
        },
        'django.request': {
            'handlers': ['request_handler'],
            'level': 'INFO',
            'propagate': True
        },
        'TestingRunner': {
            'handlers': ['scprits_handler', 'console'],
            'level': 'INFO',
            'propagate': True
        }
    }
}
