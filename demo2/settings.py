"""
Django settings for demo2 project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_lsu)9-ec%htb@0p_8!=5ft%j(qnt7u8b27#tw2c)9^=1c2#f+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'gift_search',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social.apps.django_app.default',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # PYTHON SOCIAL AUTH #
    'social.apps.django_app.middleware.SocialAuthExceptionMiddleware'
)

ROOT_URLCONF = 'demo2.urls'

WSGI_APPLICATION = 'demo2.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

#AUTH MODEL
AUTH_USER_MODEL = 'gift_search.User'
LOGIN_URL = '/'


#PYTHON SOCIAL AUTH #
# TEMPLATE_CONTEXT_PROCESSORS = (
#     'django.contrib.auth.context_processors.auth',
#     'social.apps.django_app.context_processors.backends',
#     'social.apps.django_app.context_processors.login_redirect',
# )

#Google AUTH #

# AUTHENTICATION_BACKENDS = (
#     # 'social.backends.facebook.FacebookOAuth2',
#     'django.contrib.auth.backends.ModelBackend',
#     'social.backends.google.GooglePlusAuth',
# )

# SOCIAL_AUTH_FACEBOOK_KEY = '801249369938630'
# SOCIAL_AUTH_FACEBOOK_SECRET = '47658630be8efa825387db72764385d8'
# SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', 'public_profile', 'user_photos', 'user_friends']
# SOCIAL_AUTH_FACEBOOK_EXTRA_DATA = []

#GOOGLE AUTH#
# SOCIAL_AUTH_GOOGLE_PLUS_KEY = '337098422696-gn08i76vdoatrrcchoh63f37qtqd8c30.apps.googleusercontent.com'
# SOCIAL_AUTH_GOOGLE_PLUS_SECRET = 'GgBK3NkQaoKMTSvJLRnR_FoW'
# LOGIN_REDIRECT_URL = 'friends'


#AMAZONAPI#
AMAZON_ACCESS_KEY = 'AKIAIWQB252PBOI3WW3A'
AMAZON_SECRET_KEY = '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'
AMAZON_ASSOC_TAG = 'birtgift0e-20'

#amazonproduct
config = {
    'access_key': 'AKIAIWQB252PBOI3WW3A',
    'secret_key': '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',
    'associate_tag': 'birtgift0e-20',
    'locale': 'us'
}

try:
    from local_settings import *
except ImportError:
    pass