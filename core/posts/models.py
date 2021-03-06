from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit

from core.accounts.models import User


class Post(models.Model):
    object_id = models.CharField(max_length=11, null=False, blank=False)
    user = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING)
    image = ProcessedImageField(
        upload_to="uploads/posts/images/",
        processors=[ResizeToFit(480, 600)],
        format="JPEG",
        options={"quality": 90},
        null=True,
    )
    caption = models.TextField(null=True, blank=True)
    date_created = models.DateField(auto_now_add=True, null=True, blank=True)
    datetime_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_bulletin = models.BooleanField(default=True)


class Tag(models.Model):
    object_id = models.CharField(max_length=11, null=True, blank=True)
    name = models.CharField(max_length=300, null=False, blank=False)

    def __str__(self):
        return self.name


class PostTag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name="hashtag",
        max_length=300,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.tag.name
