import functools
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse, HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, DetailView, \
    DeleteView, ListView, View
from django.contrib.auth.mixins import PermissionRequiredMixin
from gramm_app.models import Post, Like
from gramm_app.forms import PostCreateForm, PostUpdateForm


# Create your views here.


def index(request):
    if request.user.is_authenticated:
        return redirect('post-list')
    return render(request, 'gramm_app/index.html')


class PostCreateView(PermissionRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    permission_required = 'gramm_app.add_post'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.pk})

    def has_permission(self):
        perms = self.get_permission_required()
        return self.request.user.has_perms(perms)


class PostDetailView(PermissionRequiredMixin, DetailView):
    model = Post
    fields = ['title', 'image']
    permission_required = 'gramm_app.view_post'
    permission_denied_message = "You can't view this post"


class PostUpdateView(PermissionRequiredMixin, UpdateView):
    template_name_suffix = '_update_form'
    model = Post
    form_class = PostUpdateForm
    permission_required = 'gramm_app.change_post'
    permission_denied_message = 'You are have not permissions'

    def has_permission(self):
        perms = self.get_permission_required()
        objects_author = self.model.objects \
            .get(pk=self.kwargs.get('pk')) \
            .author
        return self.request.user.has_perms(perms) and (
                    objects_author == self.request.user)

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.id})

    def handle_no_permission(self):
        messages.warning(self.request,
                         'You are have not permissions to do this.')

        return HttpResponseRedirect(reverse('post-detail',
                                            kwargs={
                                                'pk': self.kwargs.get('pk')
                                            }))


class PostDeleteView(PermissionRequiredMixin, DeleteView):
    model = Post
    permission_required = 'gramm_app.delete_post'

    def get_success_url(self):
        return reverse('index')


class PostListView(PermissionRequiredMixin, ListView):
    permission_required = 'gramm_app.view_post'
    model = Post
    queryset = model.objects.all().order_by('id')
    paginate_by = 9

    def has_permission(self):
        perms = self.get_permission_required()
        return self.request.user.has_perms(perms)


class LikeView(PermissionRequiredMixin, View):
    permission_required = 'gramm_app.view_post'
    post_model = Post

    @functools.cached_property
    def user_model(self):
        return get_user_model()

    def get(self, request, pk):
        post = Post.objects.get(id=pk)
        viewer = self.user_model.objects.get(id=request.user.pk)
        is_liker = post.is_liked(viewer)
        if not is_liker:
            Like.like(viewer, post)
        else:
            post.likes.get(liker_id=viewer.id).delete()
        return JsonResponse({
            "likes_count": post.likes.count(),
            "is_liker": post.is_liked(viewer)},
            status=200)
