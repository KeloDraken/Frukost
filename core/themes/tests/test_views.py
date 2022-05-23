from django.test import Client, TestCase
from django.urls import reverse

from core.accounts.models import User


class TestThemesViews(TestCase):
    def setUp(self):
        """
        It creates a user with the username "test" and password "kgosiemang100" and then creates a client object
        """
        self.user = User.objects.create_user(username="test", password="kgosiemang100")
        self.client = Client()

    def test_themes_page_user_logged_out(self):
        url = reverse("themes:get-themes")
        response = self.client.get(url)
        self.assertRedirects(response, "/u/login/")
        self.assertEqual(response.status_code, 302)

    def test_themes_page_user(self):
        self.client.login(username="test", password="kgosiemang100")
        user = User.objects.all()[0]
        self.assertTrue(user.is_authenticated)

        url = reverse("themes:get-themes")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "private/themes/themes.html")
        self.assertContains(response, "You're unique, your profile should be too")
