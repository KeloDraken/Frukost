from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit

from vetkoek.core.accounts.models import User


class Community(models.Model):
    object_id = models.CharField(max_length=11, null=False, blank=False)
    user = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=140, null=False, blank=False)
    image = ProcessedImageField(
        upload_to="posts/images/",
        processors=[ResizeToFit(480, 600)],
        format="JPEG",
        options={"quality": 90},
        null=True,
    )
    date_created = models.DateField(auto_now_add=True, null=True, blank=True)
    datetime_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
