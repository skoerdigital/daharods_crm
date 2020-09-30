class JsonNotFound(Exception):

    def __init__(self):

        Exception.__init__(self, 'Record not found')

class DisableCSRF(object):
    def process_request(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)