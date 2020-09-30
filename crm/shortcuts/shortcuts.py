import json
from django.shortcuts import _get_queryset
from django.http import HttpResponse
from crm.exceptions.custom import JsonNotFound



def get_object_or_json404(klass, *args, **kwargs):
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        raise JsonNotFound()

def render_to_json_response(context, **response_kwargs):
    response_kwargs['content_type'] = 'application/json'
    return HttpResponse(convert_context_to_json(context), **response_kwargs)


def convert_context_to_json(context):
    return json.dumps(context)