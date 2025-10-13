"""
Settings package initialization.
Automatically loads the correct settings module based on DJANGO_ENV environment variable.
"""
import os
from decouple import config

# Get environment (defaults to 'development')
ENV = config('DJANGO_ENV', default='development')

if ENV == 'production':
    from .production import *
elif ENV == 'development':
    from .development import *
else:
    from .base import *

