from __future__ import absolute_import
from .base import *



# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from crm.celery import app as celery_app

# from .production import *

# try:
#    from .local import *
# except:
#    pass

