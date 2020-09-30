from crm.shortcuts.shortcuts import render_to_json_response

class AjaxFormResponseMixin(object):
    def form_invalid(self, form):
        return render_to_json_response(form.errors, status=400)

    def form_valid(self, form):
        self.object = form.save()
        context = {}
        return render_to_json_response(self.get_context_data(context))