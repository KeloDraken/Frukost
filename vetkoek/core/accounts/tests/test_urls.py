from django.test import TestCase
from django.urls import reverse


class TestUrls(TestCase):
    def test_register_route(self):
        url = reverse('accounts:user-register')
        self.assertEqual(url, '/u/register/')

    def test_login_route(self):
        url = reverse('accounts:user-login')
        self.assertEqual(url, '/u/login/')

    def test_logout_route(self):
        url = reverse('accounts:user-logout')
        self.assertEqual(url, '/u/logout/')

    def test_edit_route(self):
        url = reverse('accounts:edit-user-profile')
        self.assertEqual(url, '/u/edit/')

    def test_explore_route(self):
        url = reverse('accounts:explore-users')
        self.assertEqual(url, '/u/explore/')

    def test_upgrade_route(self):
        url = reverse('accounts:upgrade')
        self.assertEqual(url, '/u/upgrade/')

    def test_delete_route(self):
        url = reverse('accounts:delete-user')
        self.assertEqual(url, '/u/delete/')


