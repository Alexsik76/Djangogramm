from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, ListView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from gramm_app.models import Post
from gramm_app.forms import PostCreateForm, PostUpdateForm

# Create your views here.


def index(request):
    return render(request, 'gramm_app/index.html')


class PostCreateView(PermissionRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    permission_required = 'auth_by_email.gramm_app.create_post'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.pk})


class PostDetailView(PermissionRequiredMixin, DetailView):
    model = Post
    fields = ['title', 'image']
    permission_required = 'auth_by_email.gramm_app.view_post'
    permission_denied_message = "You can't view this post"


class PostUpdateView(PermissionRequiredMixin, UpdateView):
    template_name_suffix = '_update_form'
    model = Post
    form_class = PostUpdateForm
    permission_required = 'auth_by_email.gramm_app.edit_post'

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.pk})


class PostDeleteView(PermissionRequiredMixin, DeleteView):
    model = Post
    permission_required = 'auth_by_email.gramm_app.delete_post'

    def get_success_url(self):
        return reverse('index')


class PostListView(PermissionRequiredMixin, ListView):
    permission_required = 'auth_by_email.gramm_app.view_posts'
    model = Post


