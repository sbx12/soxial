from django.shortcuts import render
from django.views import generic

# Models
from django.contrib.auth.models import User


class ProfileView(generic.TemplateView):
    template_name = "profiles/profile_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    
class PublicProfileView(generic.DetailView):
    model = User
    context_object_name = 'user'
    template_name = "profiles/public_profile_page.html"