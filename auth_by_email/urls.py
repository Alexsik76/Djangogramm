from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from . import views

urlpatterns = [
    path('signup/', views.Signup.as_view(), name='signup'),
    path('activate/<str:uidb64>/<str:token>/', views.Activate.as_view(), name='activate'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(), name='login'),
    path('user_detail<int:pk>/', views.DjUserDetailView.as_view(), name='user_detail'),
    path('user_update/', views.DjUserUpdateView.as_view(), name='user_update'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('follow<int:pk>/', views.FollowView.as_view(), name='following')
]
