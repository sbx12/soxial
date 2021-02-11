from django.shortcuts import render
from django.views import generic


class ProfileView(generic.TemplateView):
    template_name = "profiles/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context