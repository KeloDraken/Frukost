from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse
from imagekit.models.fields import ProcessedImageFieldFile

from core.accounts.models import User
from core.accounts.views import is_dirty_html


class TestAccountsViews(TestCase):
    def setUp(self):
        """
        It creates a user with the username "test" and password "kgosiemang100" and then creates a client object
        """
        self.user = User.objects.create_user(username="test", password="kgosiemang100")
        self.client = Client()

    def test_dirty_html(self):
        html: str = "<script>alert('test');</script>"
        result: bool = is_dirty_html(html)
        self.assertTrue(result)

    def test_get_user_profile(self):
        response = self.client.get(reverse("at-get-user", kwargs={"username": "test"}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "public/user_profile.html")
        self.assertContains(response, "test")

    def test_get_no_such_user(self):
        response = self.client.get(reverse("at-get-user", kwargs={"username": "test1"}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "public/404.html")
        self.assertContains(response, "Page Not Found")

    def test_register_page(self):
        """
        We are testing the register page, which is the url "accounts:user-register" and we are checking that the response is
        200, that the template used is "public/auth/registration_form.html" and that the response contains the text "Create
        an account on Frukost"
        """
        url = reverse("accounts:user-register")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "public/auth/registration_form.html")
        self.assertContains(response, "Create an account on Frukost")

    def test_username_taken(self):
        """
        We are testing that when a user tries to register with a username that is already taken, they are redirected to the
        registration page with an error message
        """
        response = self.client.post(
            reverse("accounts:user-register"),
            {"username": "test", "password1": "kgosiemang100"},
        )
        self.assertTemplateUsed(response, "public/auth/registration_form.html")
        self.assertContains(
            response, "This username is not available, please try another one."
        )

    def test_password_no_match(self):
        """
        The function tests if the password fields match
        """
        response = self.client.post(
            reverse("accounts:user-register"),
            {
                "username": "test",
                "password1": "kgosiemang100",
                "password2": "password12454",
            },
        )
        self.assertTemplateUsed(response, "public/auth/registration_form.html")
        self.assertContains(response, "The two password fields didn’t match.")

    def test_user_created(self):
        """
        We are testing that when a user registers, the number of users in the database increases by one
        """
        users = len(User.objects.all())
        self.assertEqual(users, 1)

        response = self.client.post(
            reverse("accounts:user-register"),
            {
                "username": "test1",
                "password1": "kgosiemang100",
                "password2": "kgosiemang100",
            },
        )

        users = len(User.objects.all())
        self.assertEqual(users, 2)
        self.assertRedirects(response, "/f/")

    def test_login_page(self):
        """
        We're testing the login page, so we're going to check that the login page is accessible, that the correct template
        is used, and that the page contains the text "Sign In"
        """
        url = reverse("accounts:user-login")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "public/auth/login_form.html")
        self.assertContains(response, "Sign In")

    def test_user_login(self):
        """
        The function tests if a user can login to the system
        """
        self.client.login(username="test", password="kgosiemang100")
        user = User.objects.all()[0]
        self.assertTrue(user.is_authenticated)

    def test_user_login_incorrect(self):
        """
        The function tests that when a user tries to log in with incorrect credentials, the user is redirected to the login
        page with an error message
        """
        response = self.client.post(
            reverse("accounts:user-login"),
            {"username": "test1", "password": "kgosiemang100"},
        )
        self.assertTemplateUsed(response, "public/auth/login_form.html")
        self.assertContains(response, "Incorrect log in credentials")

    def test_edit_profile_pic(self):
        """
        The function tests if a user can edit their profile picture
        """
        self.client.login(username="test", password="kgosiemang100")
        profile_pic = SimpleUploadedFile(
            "anime.jpg", b"file_content", content_type="image/jpeg"
        )
        self.client.post(
            reverse("accounts:edit-user-profile"), {"profile-pic": profile_pic}
        )
        user = User.objects.get(username="test")
        self.assertTrue(isinstance(user, User))
        u_profile_pic = user.profile_pic
        self.assertEqual(type(u_profile_pic), ProcessedImageFieldFile)
