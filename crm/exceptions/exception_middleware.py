
from django.utils import timezone
from django.utils.dateformat import format
from django.conf import settings
from crm.exceptions.custom import JsonNotFound
from crm.shortcuts.shortcuts import render_to_json_response


class ExceptionMiddleware(object):

    def process_exception(self, request, exception):
        if type(exception) == JsonNotFound:
            now = format(timezone.now(), u'U')
            kwargs = {}
            response = {
                'status': '404',
                'message': 'Record not found',
                'timestamp': now,
                'errorcode': settings.API_ERROR_RECORD_NOT_FOUND
            }
            return render_to_json_response(response, status=404, **kwargs)
        return None