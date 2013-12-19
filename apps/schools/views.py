from django.views.generic import View, FormView, TemplateView


class HomeView(TemplateView):
    template_name = "index.html"
