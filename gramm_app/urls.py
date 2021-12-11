from django.urls import path
from .views import index, PostCreateView, PostDetailView, PostUpdateView, PostDeleteView, PostListView, LikeView

urlpatterns = [
    path('', index, name='index'),
    path('create_post/', PostCreateView.as_view(), name='post-create'),
    path('detail_post/<int:pk>', PostDetailView.as_view(), name='post-detail'),
    path('update_post/<int:pk>', PostUpdateView.as_view(), name='post-update'),
    path('delete_post/<int:pk>', PostDeleteView.as_view(), name='post-delete'),
    path('posts/', PostListView.as_view(), name='post-list'),
    path('post_like/<int:pk>', LikeView.as_view(), name='post-like'),
]
