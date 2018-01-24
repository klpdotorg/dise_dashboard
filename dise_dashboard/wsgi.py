"""
WSGI config for dise_dashboard project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os
import sys
import time
import traceback
import signal

PROJECT_ROOT = os.path.realpath(os.path.dirname(os.path.dirname(__file__)))

sys.path.append(PROJECT_ROOT)

# We defer to a DJANGO_SETTINGS_MODULE already in the environment. This breaks
# if running multiple sites in the same mod_wsgi process. To fix this, use
# mod_wsgi daemon mode with each site in its own daemon process, or use
# os.environ["DJANGO_SETTINGS_MODULE"] = "dise_dashboard.settings"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dise_dashboard.settings")
sys.path.append(os.path.join(os.getcwd(), 'apps'))

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application

try:
    application = get_wsgi_application()
    print 'WSGI without exception'
except Exception:
    print 'handling WSGI exception'
    # Error loading applications
    if 'mod_wsgi' in sys.modules:
        traceback.print_exc()
        os.kill(os.getpid(), signal.SIGINT)
        time.sleep(2)
