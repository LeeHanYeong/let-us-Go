from rest_framework.renderers import BrowsableAPIRenderer


class BrowsableAPIRendererWithoutForms(BrowsableAPIRenderer):
    def get_context(self, *args, **kwargs):
        context = super(BrowsableAPIRendererWithoutForms, self).get_context(
            *args, **kwargs
        )
        context["display_edit_forms"] = False
        return context

    def get_filter_form(self, data, view, request):
        return None

    def get_rendered_html_form(self, data, view, method, request):
        return None
