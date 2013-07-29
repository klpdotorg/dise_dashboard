from django.views.generic import View, FormView, TemplateView


class SearchView(TemplateView):
    template_name = "schools/search.html"
