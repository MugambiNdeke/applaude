import os
from django.core.wsgi import get_wsgi_application

# Point to the correct settings file
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'applaude.settings')

application = get_wsgi_application()
