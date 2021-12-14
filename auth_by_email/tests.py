from django.test import TestCase, Client
from django.urls import reverse
from django.core.exceptions import ValidationError
from auth_by_email.models import DjGrammUser, Following
import random
import cloudinary
from cloudinary import CloudinaryResource
from cloudinary.models import CloudinaryField

# Create your tests here.
SUFFIX = random.randint(10000, 99999)
API_TEST_ID = "dj_test_{}".format(SUFFIX)


class SignupViewTest(TestCase):
    def test_signup(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)


class AllAuthByEmailViewsTest(TestCase):
    def setUp(self) -> None:
        cloudinary.config(cloud_name='dgh6qdngr')
        user = DjGrammUser.objects._create_user(id=1,
                                                email='example@email.com',
                                                bio='mister',
                                                avatar="image/upload/v1234/{}.jpg".format(API_TEST_ID),
                                                first_name='John',
                                                last_name='Snow',
                                                password='password12')
        user.grant_user_permissions()
        self.user_id = 1

    def test_logout(self):
        c = Client()
        c.login(email='example@email.com', password='password12')
        response = c.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)

    def test_to_python(self):
        c = CloudinaryField('image')
        res = CloudinaryResource(public_id=API_TEST_ID, format='jpg')
        # Can't compare the objects, so compare url instead
        self.assertEqual(c.to_python('{}.jpg'.format(API_TEST_ID)).build_url(), res.build_url())

    def test_user_image_field(self):
        user = DjGrammUser.objects.get(email='example@email.com')
        self.assertIsNotNone(user)
        self.assertEqual(user.avatar.public_id, API_TEST_ID)
        self.assertTrue(False or user.avatar)

    def test_user_detail(self):
        c = Client()
        c.login(email='example@email.com', password='password12')
        response = c.get(reverse('user_detail', args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_user_update(self):
        c = Client()
        c.login(email='example@email.com', password='password12')
        response = c.get(reverse('user_update'))
        self.assertEqual(response.status_code, 200)

    def test_password_reset(self):
        c = Client()
        c.login(email='example@email.com', password='password12')
        response = c.get(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)

    def test_password_reset_done(self):
        c = Client()
        c.login(email='example@email.com', password='password12')
        response = c.get(reverse('password_reset_done'))
        self.assertEqual(response.status_code, 200)

    def test_password_reset_complete(self):
        c = Client()
        c.login(email='example@email.com', password='password12')
        response = c.get(reverse('password_reset_complete'))
        self.assertEqual(response.status_code, 200)

    def test_follow_view(self):
        c = Client(HTTP_REFERER=reverse('signup'))
        c.login(email='example@email.com', password='password12')
        response = c.get(reverse('follow', args=[1]))
        self.assertEqual(response.status_code, 302)

    def test_unfollow(self):
        c = Client(HTTP_REFERER=reverse('signup'))
        c.login(email='example@email.com', password='password12')
        response = c.get(reverse('unfollow', args=[1]))
        self.assertEqual(response.status_code, 302)


class DjUserModelTest(TestCase):
    def setUp(self) -> None:
        user = DjGrammUser.objects._create_user(email='example@email.com',
                                                bio='mister',
                                                avatar='picture.png',
                                                first_name='John',
                                                last_name='Snow',
                                                password='password12')
        user.grant_user_permissions()
        DjGrammUser.objects.create_superuser(email='admin@email.com',
                                             password='adminpassword')

    def test_create_superuser(self):
        admin = DjGrammUser.objects.get(email='admin@email.com')
        self.assertTrue(admin.is_superuser)

    def test_user_ful_name(self):
        john = DjGrammUser.objects.get(first_name='John')
        self.assertEqual(john.get_full_name(), 'John Snow')

    def test_user_permissions(self):
        user = DjGrammUser.objects.get(first_name='John')
        self.assertEqual(user.has_perm('gramm_app.add_post'), True)
        self.assertEqual(user.has_perm('gramm_app.change_post'), True)
        self.assertEqual(user.has_perm('gramm_app.view_post'), True)
        self.assertEqual(user.has_perm('gramm_app.delete_post'), True)

    def test_follow_self(self):
        user = DjGrammUser.objects.get(first_name='John')
        with self.assertRaises(ValidationError):
            Following.follow(user, user)
