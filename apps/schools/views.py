from django.views.generic import FormView, TemplateView
from .forms import SearchForm


class SearchView(FormView):
    form_class = SearchForm
    template_name = "schools/search.html"