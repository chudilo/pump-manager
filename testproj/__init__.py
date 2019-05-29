# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.


from __future__ import absolute_import
from .clr import app as celery_app

#x = 10

__all__ = ('celery_app',)
