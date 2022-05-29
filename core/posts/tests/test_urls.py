from django.test import TestCase
from django.urls import reverse


class TestPostUrls(TestCase):
    def test_frontpage_url(self):
        url = reverse("posts:frontpage")
        self.assertEqual("/f/", url)

    def test_create_post_url(self):
        url = reverse("posts:create-post")
        self.assertEqual("/f/add/", url)

    def test_delete_post_url(self):
        url = reverse("posts:delete-post", kwargs={"post_id": "123456"})
        self.assertEqual("/f/delete/123456/", url)

    def test_get_post_url(self):
        url = reverse("posts:get-post", kwargs={"post_id": "123456"})
        self.assertEqual("/f/123456/", url)
