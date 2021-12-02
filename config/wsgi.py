import os
from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv
load_dotenv()

config = os.getenv('ENVIRONMENT', 'development')
django_settings_module = f'config.settings.{config}'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', django_settings_module)

application = get_wsgi_application()
