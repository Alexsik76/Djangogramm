from django.test import TestCase
from django.urls import reverse
from auth_by_email.models import DjGrammUser
from django.contrib.auth.models import Permission


# Create your tests here.

class SignupViewTest(TestCase):
    def test_signup(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)


class DjUserModelTest(TestCase):
    def setUp(self) -> None:
        DjGrammUser.objects._create_user(email='example@email.com',
                                         bio='mister',
                                         avatar='picture.png',
                                         first_name='John',
                                         last_name='Snow',
                                         password='password12'
                                         )

    def test_user_ful_name(self):
        john = DjGrammUser.objects.get(first_name='John')
        self.assertEqual(john.get_full_name(), 'John Snow')

    # def test_user_permissions(self):
    #     user = DjGrammUser.objects.get(first_name='John')
    #     user.grant_user_permissions()
    #     self.assertEqual(user.has_perm('auth_by_email.gramm_app.create_post'), True)

