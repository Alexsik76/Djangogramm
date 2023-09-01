from django.contrib.auth import get_user_model, login, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import UpdateView, DetailView
from .forms import SignupForm, UserActivationForm, UserUpdateForm
from .utils import create_email


class Signup(View):
    form_class = SignupForm
    template_name = 'registration/signup.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        domain = get_current_site(request).domain
        if form.is_valid():
            message = self.make_first_registration_message(form, domain)
            message.send(fail_silently=False)
            return render(request, 'registration/signup_done.html')
        else:
            email = form.data.get('email', None)
            match self.get_email_status(email):
                case 'not_registered':
                    return render(request, self.template_name, {'form': form})
                case 'activated':
                    return redirect('login', permanent=True)
                case 'not_activated':
                    message = self.remake_registration_message(email, domain)
                    message.send(fail_silently=False)
                    return render(request, 'registration/resign_up_done.html')

    @staticmethod
    def get_email_status(email):
        if DjGrammUser.objects.filter(email=email).exists():
            user = DjGrammUser.objects.get(email=email)
            return 'activated' if user.is_active else 'not_activated'
        else:
            return 'not_registered'

    @staticmethod
    def make_first_registration_message(form, domain):
        user = form.save(commit=False)
        user.make_inactive_user()
        user.save()
        message = create_email(user, domain)
        return message

    @staticmethod
    def remake_registration_message(email, domain):
        user = DjGrammUser.objects.get(email=email)
        message = create_email(user, domain)
        return message

# TODO: Rewrite test for the SignUp View


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
            update_session_auth_hash(request, user)
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
            viewer.follow(author)
        except ValidationError as e:
            return JsonResponse({'message': e.message}, status=403)
        return JsonResponse({
            "count": author.followers.count(),
            "is_followed": author.is_followed(viewer)
        })
