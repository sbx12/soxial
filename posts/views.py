from django.views import generic
from django.urls import reverse
from django.contrib import messages

# Models
from posts.models import Post

# Forms
from posts.forms import CreatePostForm

class CreatePostView(generic.CreateView):
    model = Post
    form_class = CreatePostForm
    template_name = "posts/create_post_page.html"
    
    def form_valid(self, form):
        post = form.save()
        messages.success(self.request, 'New Post Created')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('profile')