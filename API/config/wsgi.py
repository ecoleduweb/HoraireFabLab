"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
import pymysql
pymysql.install_as_MySQLdb()

import MySQLdb
MySQLdb.__version__ = "2.2.1"
MySQLdb.version_info = (2, 2, 1, "final", 0)
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
