from django.contrib import messages
from django.contrib.auth import get_user_model, login, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import UpdateView, DetailView
from .forms import SignupForm, UserActivationForm, UserUpdateForm
from .models import Following
from utils import create_inactive_user, create_mesage_body

# Create your views here.


class Signup(View):
    form_class = SignupForm
    template_name = 'registration/signup.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = create_inactive_user(form)
            user.save()
            message_body = create_mesage_body(user, request)
            to_email = user.email
            email = EmailMessage(subject='Activate your account.',
                                 body=message_body,
                                 to=[to_email])
            email.send(fail_silently=False)
            return render(request, 'registration/signup_done.html')
        else:
            return render(request, self.template_name, {'form': form})


DjGrammUser = get_user_model()


class Activate(View):
    form_class = UserActivationForm
    template_name = 'registration/activation.html'

    def get(self, request, *args, **kwargs):
        assert 'uidb64' in kwargs and 'token' in kwargs
        try:
            uid = urlsafe_base64_decode(kwargs['uidb64']).decode()
            user = DjGrammUser.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, DjGrammUser.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, kwargs['token']):
            # activate user and login:
            user.is_active = True
            user.save()
            login(request, user)
            form = self.form_class(instance=request.user)
            return render(request, self.template_name, {'form': form})

        else:
            return HttpResponse('Activation link is invalid!')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST,
                               request.FILES,
                               instance=request.user)
        if form.is_valid():
            user = form.save()
            user.grant_user_permissions()
            user.save()
            update_session_auth_hash(request, user)  # Important, to update the session with the new password
            return redirect('index')
        else:
            return render(request, self.template_name, {'form': form})


class DjUserDetailView(LoginRequiredMixin, DetailView):
    model = DjGrammUser
    context_object_name = 'dj_user'
    template_name = 'registration/user_detail.html'


class DjUserUpdateView(LoginRequiredMixin, UpdateView):
    model = DjGrammUser
    template_name = 'registration/user_update.html'
    form_class = UserUpdateForm

    def get_object(self, *args, **kwargs):
        return self.request.user

    def get_success_url(self):
        return reverse('user_detail',  kwargs={'pk': self.request.user.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object() # noqa
        form = self.get_form()
        if not form.has_changed():
            return redirect(self.get_success_url())
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class FollowingView(LoginRequiredMixin, View):
    object = DjGrammUser

    def get(self, request, pk, *args, **kwargs):
        author = self.object.objects.get(pk=pk)
        viewer = self.object.objects.get(pk=request.user.id)
        try:
            Following.follow(author, viewer)
        except IntegrityError:
            follower = author.followers.get(follower_user=viewer)
            Following.unfollow(follower)
        except ValidationError as e:
            return JsonResponse({'error_message': e.message}, status=403)
        return JsonResponse({
            "count": author.followers.count(),
            "is_followed": author.is_followed(viewer)},
            status=200)
