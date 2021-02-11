from django.shortcuts import render
from django.views import generic


class HomeView(generic.TemplateView):
    template_name = "home/pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context