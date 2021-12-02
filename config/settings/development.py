from .base import *
import os


DEBUG = True

INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

# FIXTURE_DIRS = ['cre_finance/apps/cre_finance/fixtures/']
