from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from auth_by_email.models import DjGrammUser


class SignupForm(forms.ModelForm):

    class Meta:
        model = DjGrammUser
        fields = ('email',)
        help_texts = {
            'email': 'Enter your email address here',
        }


class UserActivationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['avatar'].widget.template_name = 'auth_by_email/bulma_templates/widgets/clearable_file_input.html'
        self.fields['bio'].widget.template_name = 'auth_by_email/bulma_templates/widgets/select.html'

    class Meta:
        model = DjGrammUser
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2',  'bio', 'avatar')

    class Media:
        js = ('forms/file_field.js',)


class UserUpdateForm(UserChangeForm):
    password = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['avatar'].widget.template_name = 'auth_by_email/bulma_templates/widgets/clearable_file_input.html'
        self.fields['bio'].widget.template_name = 'auth_by_email/bulma_templates/widgets/select.html'

    class Meta(UserActivationForm.Meta):
        fields = ('first_name', 'last_name', 'email', 'bio', 'avatar')

    class Media:
        js = ('forms/file_field.js',)


class LoginForm(AuthenticationForm):

    class Meta:
        model = DjGrammUser
        fields = ('email', 'password')


