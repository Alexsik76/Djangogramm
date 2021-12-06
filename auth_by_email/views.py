from django.contrib import messages
from django.contrib.auth import get_user_model, login, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import UpdateView, DetailView

from .forms import SignupForm, UserActivationForm, UserUpdateForm


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
            # Create an inactive user with no password:
            user = form.save(commit=False)
            user.is_active = False
            user.set_unusable_password()
            user.username = user.email
            user.save()
            # Send an email to the user with the token:
            mail_subject = 'Activate your account.'
            message = render_to_string('registration/activation_email.html', {
                'user': user,
                'domain': get_current_site(request).domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
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
            messages.success(request, f'You are successful login as {user.get_full_name()}.')
            return redirect('index')
        else:
            return render(request, self.template_name, {'form': form})


class DjUserDetailView(LoginRequiredMixin, DetailView):
    model = DjGrammUser
    context_object_name = 'dj_user'
    template_name = 'registration/user_detail.html'

    def get_object(self, *args, **kwargs):
        return self.request.user


class DjUserUpdateView(LoginRequiredMixin, UpdateView):
    object: object
    model = DjGrammUser
    template_name = 'registration/user_update.html'
    form_class = UserUpdateForm

    def get_object(self, *args, **kwargs):
        return self.request.user

    def get_success_url(self):
        return reverse('user_detail')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if not form.has_changed():
            return redirect(self.get_success_url())
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
