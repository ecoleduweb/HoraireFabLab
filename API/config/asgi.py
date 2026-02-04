"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
import pymysql
pymysql.install_as_MySQLdb()

import MySQLdb
MySQLdb.__version__ = "2.2.1"
MySQLdb.version_info = (2, 2, 1, "final", 0)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_asgi_application()
