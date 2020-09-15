"""
WSGI config for kbboard project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os, sys

# Эти пути необходимы для работы на бое в режиме mod_wsgi как демона.
# Решают проблему ModuleNotFoundError: No module named 'имя_модуля'
sys.path.append('/home/cyberbotx/.local/lib/python3.6/site-packages')
sys.path.append('/var/www/kanban-board.bot.net')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kbboard.settings')

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
