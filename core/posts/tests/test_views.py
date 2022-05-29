from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponseRedirect
from django.test import Client, TestCase
from django.urls import reverse

from core.accounts.models import User
from core.posts.models import Post


class TestPostViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="kgosiemang100")
        self.client = Client()

    def test_post_upload_not_logged_in(self):
        image = SimpleUploadedFile(
            "anime.jpg", b"file_content", content_type="image/jpeg"
        )
        posts = len(Post.objects.all())
        self.assertEqual(0, posts)

        response = self.client.post(
            reverse("posts:create-post"), {"user": "test", "caption": "", "image": image}
        )
        self.assertEqual("/u/login/?next=/f/add/", response.url)
