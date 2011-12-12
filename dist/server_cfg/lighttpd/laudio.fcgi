#!/usr/bin/python2
import sys, os

# Add application root to PYTHON_PATH
sys.path.insert(0, "/usr/share/laudio")

# Setup Django
from django.core.servers.fastcgi import runfastcgi
os.environ['DJANGO_SETTINGS_MODULE'] = "laudio.settings"
runfastcgi(method="threaded", daemonize="false")
