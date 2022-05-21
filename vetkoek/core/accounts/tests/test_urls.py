from django.test import TestCase
from django.urls import reverse


class TestUrls(TestCase):
    def test_register_route(self):
        """
        It asserts that the url for the user-register view is equal to /u/register/
        """
        url = reverse("accounts:user-register")
        self.assertEqual(url, "/u/register/")

    def test_login_route(self):
        """
        It asserts that the url of the login route is equal to "/u/login/"
        """
        url = reverse("accounts:user-login")
        self.assertEqual(url, "/u/login/")

    def test_logout_route(self):
        """
        It tests that the url for the logout route is equal to "/u/logout/"
        """
        url = reverse("accounts:user-logout")
        self.assertEqual(url, "/u/logout/")

    def test_edit_route(self):
        """
        This tests that the url for the edit-user-profile view is /u/edit/
        """
        url = reverse("accounts:edit-user-profile")
        self.assertEqual(url, "/u/edit/")

    def test_explore_route(self):
        """
        It tests that the url for the explore-users view is equal to /u/explore/
        """
        url = reverse("accounts:explore-users")
        self.assertEqual(url, "/u/explore/")

    def test_upgrade_route(self):
        url = reverse("accounts:upgrade")
        self.assertEqual(url, "/u/upgrade/")

    def test_delete_route(self):
        url = reverse("accounts:delete-user")
        self.assertEqual(url, "/u/delete/")

    def test_themes_route(self):
        url = reverse("accounts:user-themes")
        self.assertEqual(url, "/u/themes/")
