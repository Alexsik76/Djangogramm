import functools
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, ListView, View
from django.contrib.auth.mixins import PermissionRequiredMixin
from gramm_app.models import Post, Like
from gramm_app.forms import PostCreateForm, PostUpdateForm
from asgiref.sync import sync_to_async
import json


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

    def has_permission(self):
        perms = self.get_permission_required()
        objects_author = self.model.objects.get(pk=self.kwargs.get('pk')).author
        return self.request.user.has_perms(perms) and (objects_author == self.request.user)

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.pk})


class PostDeleteView(PermissionRequiredMixin, DeleteView):
    model = Post
    permission_required = 'gramm_app.delete_post'

    def get_success_url(self):
        return reverse('index')


class PostListView(PermissionRequiredMixin, ListView):
    permission_required = 'gramm_app.view_post'
    model = Post
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

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        post = self.post_model.objects.get(pk=pk)
        viewer = self.user_model.objects.get(pk=request.user.id)
        try:
            Like.like(viewer, post)
            messages.success(request, f'You are like the {post.title}.')
        except IntegrityError:
            messages.warning(request, f'You are already like the {post.title}.')
        except ValidationError as e:
            messages.warning(request, e.message)
        return redirect(request.META['HTTP_REFERER'])


class LikeView2(PermissionRequiredMixin, View):
    permission_required = 'gramm_app.view_post'
    post_model = Post

    @functools.cached_property
    def user_model(self):
        return get_user_model()

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        post = self.post_model.objects.get(pk=pk)
        is_liker = post.likes.filter(liker_id=request.user.id).exists()
        likes_count = post.likes.count()
        return JsonResponse({'liker': is_liker,
                             'likes': likes_count})

    def post(self, request, *args, **kwargs):
        viewer = self.user_model.objects.get(pk=request.user.pk)
        post = Post.objects.get(pk=kwargs.get('pk'))
        is_liker = post.is_liked(viewer)
        try:
            if not is_liker:
                Like.like(viewer, post)
                messages.success(request, f'You are like the {post.title}.')
            else:
                like = Like.objects.filter(liker_id=request.user.id).first()
                like.delete()
                messages.warning(request, f'You are unlike the {post.title}.')
        except IntegrityError:
            messages.warning(request, f'You are already like the {post.title}.')
        except ValidationError as e:
            messages.warning(request, e.message)
        return HttpResponse(status=200)


@sync_to_async
def is_was_liker(request, pk):
    post = Post.objects.get(pk=pk)
    is_liker = post.likes.filter(liker_id=request.user.id).exists()
    likes_count = post.likes.count()
    return JsonResponse({'liker': is_liker,
                         'likes': likes_count})
