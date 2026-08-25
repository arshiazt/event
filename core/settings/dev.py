from decouple import config
from .base import *

DEBUG = config('DEBUG',cast=bool,default=True)
ALLOWED_HOSTS += ['127.0.0.1','localhost']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('NAME'),
        'USER':config('USER'),
        'PASSWORD':config('PASSWORD'),
        'PORT':config('PORT'),
        'HOST':config('HOST')
    }
}