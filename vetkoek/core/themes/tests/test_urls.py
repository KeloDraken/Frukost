from django.test import TestCase
from django.urls import reverse


class TestThemesUrls(TestCase):
    def test_get_themes_route(self):
        url = reverse("themes:get-themes")
        self.assertEqual(url, "/t/")
