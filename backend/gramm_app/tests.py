from django.test import TestCase, Client
from auth_by_email.models import DjGrammUser
from django.urls import reverse

# Create your tests here.


class DjUserModelTest(TestCase):
    def setUp(self) -> None:
        user = DjGrammUser.objects._create_user(email='example@email.com',
                                                bio='Mr',
                                                avatar='picture.png',
                                                first_name='John',
                                                last_name='Snow',
                                                password='password12')
        user.grant_user_permissions()

    def test_create_post_view(self):
        c = Client()
        c.login(email='example@email.com', password='password12')
        response = c.get(reverse('post-create'))
        self.assertEqual(response.status_code, 200)

    def test_create_post_anonim(self):
        response = self.client.get(reverse('post-create'))
        self.assertEqual(response.status_code, 302)

    def test_post_list_anonim(self):
        response = self.client.get(reverse('post-list'))
        self.assertEqual(response.status_code, 302)
