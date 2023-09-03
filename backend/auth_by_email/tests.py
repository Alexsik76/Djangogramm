import django.conf
from django.test import TestCase, Client
from django.core import mail
from django.urls import reverse
from django.core.exceptions import ValidationError
from auth_by_email.models import DjGrammUser
from auth_by_email.forms import SignupForm
from auth_by_email.views import Signup
import random
import cloudinary
from cloudinary import CloudinaryResource
from cloudinary.models import CloudinaryField
from .utils import create_email

# Create your tests here.
SUFFIX = random.randint(10000, 99999)
API_TEST_ID = "dj_test_{}".format(SUFFIX)


class SignupViewTest(TestCase):
    def setUp(self) -> None:
        self.form = SignupForm(data={'email': 'example@email.com'})
        self.user = self.form.save(commit=False)
        self.user.make_inactive_user()
        self.user.save()
        self.from_email = \
            django.conf.settings.DEFAULT_FROM_EMAIL or 'test@email'

    def test_create_inactive_user(self):
        self.assertEqual(self.user.username, 'example@email.com')
        self.assertEqual(self.user.is_active, False)

    def test_send_email(self):
        message = create_email(self.user, 'test.domain')
        message.send(fail_silently=False)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, self.from_email)
        self.assertEqual(mail.outbox[0].subject, 'Activate your account.')

    def test_signup_get(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_signup_post(self):
        response = self.client.post(reverse('signup'),
                                    data={'email': 'example@email.com'})
        self.assertContains(response,
                            'Dj gramm user with this Email address already exists, but registration is not complete.')
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('signup'),
                                    data={'email': 'example_first@email.com'})
        self.assertContains(response,
                            'We’ve emailed you instructions for the continue registration, if an account exists with '
                            'the email you entered. You should receive them shortly.')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Signup.get_email_status('wrong@email.com'), 'not_registered')
        response = self.client.post(reverse('signup'),
                                    data={'email': 'not_email.com'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].is_valid(), False)
        self.assertIn('Enter a valid email address.', response.context['form']['email'].errors)

        self.user.is_active = True
        self.user.save()
        self.assertEqual(self.user.is_active, True)
        response = self.client.post(reverse('signup'),
                                    data={'email': 'example@email.com'})
        self.assertEqual(response.status_code, 301)

    def test_get_email_status(self):
        self.assertEqual(Signup.get_email_status('wrong@email.com'), 'not_registered')
        self.assertEqual(Signup.get_email_status('example@email.com'), 'not_activated')
        self.assertEqual(self.user.is_active, False)
        self.user.is_active = True
        self.user.save()
        self.assertEqual(Signup.get_email_status('example@email.com'), 'activated')

    def test_login(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)


class AllAuthByEmailViewsTest(TestCase):
    def setUp(self) -> None:
        cloudinary.config(cloud_name='dgh6qdngr')
        user = DjGrammUser \
            .objects._create_user(id=1, email='example@email.com',
                                  bio='Mr',
                                  avatar="image/upload/v1234/{}.jpg".format(
                                      API_TEST_ID),
                                  first_name='John',
                                  last_name='Snow',
                                  password='password12')
        user.grant_user_permissions()

    def test_logout(self):
        c = Client()
        c.login(email='example@email.com', password='password12')
        response = c.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)

    def test_to_python(self):
        c = CloudinaryField('image')
        res = CloudinaryResource(public_id=API_TEST_ID, format='jpg')
        # Can't compare the objects, so compare url instead
        self.assertEqual(c.to_python('{}.jpg'.format(API_TEST_ID)).build_url(),
                         res.build_url())

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


class DjUserModelTest(TestCase):
    def setUp(self) -> None:
        user = DjGrammUser.objects._create_user(email='example@email.com',
                                                bio='Mr',
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


class FollowViewTest(TestCase):
    def setUp(self) -> None:
        self.user = \
            DjGrammUser.objects._create_user(
                id=1,
                email='example@email.com',
                bio='Mr',
                avatar='picture.png',
                first_name='John',
                last_name='Snow',
                password='password12')
        self.viewer = \
            DjGrammUser.objects._create_user(
                id=2,
                email='example2@email.com',
                bio='Mr',
                avatar='picture2.png',
                first_name='Tyrion',
                last_name='Lannister',
                password='password13')

    def test_follow_self(self):
        with self.assertRaises(ValidationError):
            self.viewer.follow(self.viewer)

    def test_follow(self):
        self.viewer.follow(self.user)
        self.assertTrue(self.user.is_followed(self.viewer))

    def test_unfollow(self):
        self.viewer.follow(self.user)
        self.viewer.unfollow(self.user)
        self.assertFalse(self.user.is_followed(self.viewer))

    def test_follow_twice(self):
        self.viewer.follow(self.user)
        self.viewer.follow(self.user)
        self.assertFalse(self.user.is_followed(self.viewer))

    def test_following_view(self):
        c = Client()
        c.login(email='example2@email.com', password='password13')
        response = c.get(reverse('following', args=[1]))
        self.assertJSONEqual(response.content,
                             {"count": 1,
                              "is_followed": True})
        response2 = c.get(reverse('following', args=[1]))
        self.assertJSONEqual(response2.content,
                             {"count": 0,
                              "is_followed": False})

        response3 = c.get(reverse('following', args=[2]))
        self.assertEqual(response3.status_code, 403)
        self.assertJSONEqual(response3.content,
                             {
                                 'message':
                                     'You can`t following yourself.'
                             })
