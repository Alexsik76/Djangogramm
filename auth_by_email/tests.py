from django.test import TestCase, Client
from django.urls import reverse
from auth_by_email.models import DjGrammUser
from gramm_app.models import Post


# Create your tests here.

class SignupViewTest(TestCase):
    def test_signup(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)


class AllAuthByEmailViewsTest(TestCase):
    def setUp(self) -> None:
        user = DjGrammUser.objects._create_user(id=1,
                                                email='example@email.com',
                                                bio='mister',
                                                avatar='picture.png',
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

    # def test_user_detail(self):
    #     c = Client(CLOUDINARY_URL='cloudinary://519678674225469:HdXa6q6uJRCtKtvpRN5SM-T1Y-c@dgh6qdngr')
    #     c.login(email='example@email.com', password='password12')
    #     response = c.get(reverse('user_detail', args=[1]))
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_user_update(self):
    #     c = Client(CLOUDINARY_URL='cloudinary://519678674225469:HdXa6q6uJRCtKtvpRN5SM-T1Y-c@dgh6qdngr')
    #     c.login(email='example@email.com', password='password12')
    #     response = c.get(reverse('user_update'))
    #     self.assertEqual(response.status_code, 200)

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

    def test_follow(self):
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

    def test_user_ful_name(self):
        john = DjGrammUser.objects.get(first_name='John')
        self.assertEqual(john.get_full_name(), 'John Snow')

    def test_user_permissions(self):
        user = DjGrammUser.objects.get(first_name='John')
        self.assertEqual(user.has_perm('gramm_app.add_post'), True)
        self.assertEqual(user.has_perm('gramm_app.change_post'), True)
        self.assertEqual(user.has_perm('gramm_app.view_post'), True)
        self.assertEqual(user.has_perm('gramm_app.delete_post'), True)

    def test_create_post(self):
        c = Client()
        c.login(email='example@email.com', password='password12')
        response = c.get(reverse('post-create'))
        self.assertEqual(response.status_code, 200)

    def test_create_post_anonimus(self):
        response = self.client.get(reverse('post-create'))
        self.assertEqual(response.status_code, 302)

    def test_post_list_anonimus(self):
        response = self.client.get(reverse('post-list'))
        self.assertEqual(response.status_code, 302)


class PostModelTest(TestCase):
    def setUp(self) -> None:
        user = DjGrammUser.objects._create_user(email='example@email.com',
                                                bio='mister',
                                                avatar='picture.png',
                                                first_name='John',
                                                last_name='Snow',
                                                password='password12'
                                                )

        self.post = Post.objects.create(title='picture',
                                        image='image.png',
                                        author=user)

    def test_delete_post(self):
        self.post.delete()
        with self.assertRaises(self.post.DoesNotExist):
            Post.objects.get(title='picture')



