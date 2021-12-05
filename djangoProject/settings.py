"""
Django settings for djangoProject project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
import datetime
import sys

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-(kv7_80+bfm9%9fzkgrb7k(2#c05r$@g(32h78$1_ame3uyrop'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# 支付宝相关配置
app_private_key_path = os.path.join(BASE_DIR, 'apps/trade/keys/private.txt')
alipay_public_key_path = os.path.join(BASE_DIR, 'apps/trade/keys/ali_public.txt')
ali_app_id = "2021000118658197"
return_url = 'http://127.0.0.1:8000/alipay/return/'
notify_url = 'http://127.0.0.1:8000/alipay/return/'

#STATIC_ROOT = os.path.join(BASE_DIR, 'collected_static')

AUTH_USER_MODEL = 'users.UserProfile'

# JWT配置
JWT_AUTH = {
    # 过期时间
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),
    # 刷新过期时间
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=30),
    # 请求头前缀
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
}

# 支付宝相关的key
private_key_path = os.path.join(BASE_DIR, 'apps/trade/keys/private.txt')
ali_pub_key_path = os.path.join(BASE_DIR, 'apps/trade/keys/ali_public.txt')

# DRF配置
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ]
}

# 手机号码验证正则表达式
REGEX_MOBILE = '^1[35789]\d{9}$|^147\d{8}$'

# 云片网APIKEY
APIKEY = 'b841697ca2c0a4c0553e5d772de4fb72'


 # 自定义用户认证配置
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'users.views.CustomBackend',
]



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.users.apps.UserConfig',
    'goods.apps.GoodsConfig',
    'trade.apps.TradeConfig',
    'user_operation',
    'DjangoUeditor',
    'xadmin',
    'notes',
    'crispy_forms',
    'rest_framework',
    'django_filters',
    'corsheaders',
    'rest_framework.authtoken',
]

# DRF配置
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ]
}

REGIX_EMAIL='^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' # 指定邮件后端
EMAIL_HOST = 'smtp.163.com' # 发邮件主机        --需要根据邮箱更改
EMAIL_PORT = 25 # 发邮件端口  /备用端口：465
EMAIL_HOST_USER = 'gomyyds@163.com' # 授权的邮箱(发送)
EMAIL_HOST_PASSWORD = 'ZLIHQZUSWSZOZNGG' # 邮箱授权时获得的密码，非注册登录密码
EMAIL_FROM = 'Lenovo<gomyyds@163.com>' # 发件人抬头 <此处要和发送邮件的邮箱相同>
SUBJECT = '邮箱验证'# 邮件标题

# 注册有效期天数
CONFIRM_DAYS = 7





MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]



ROOT_URLCONF = 'djangoProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'djangoProject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'myweb',        #数据库名
        'USER':'root',           #用户名
        'PASSWORD':'lv20010405',     #密码
        'HOST':'127.0.0.1',      #本机地址
        'PORT':'3306',           #端口
        'OPTIONS': {'init_command': 'SET default_storage_engine=INNODB;'}

    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 跨域增加忽略
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
    'token',
)