from django.contrib.auth.models import AbstractUser

from django.db import models

from django.utils.translation import gettext_lazy as _

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit

from core.accounts.validators import UnicodeEmailValidator


class LowercaseCharField(models.CharField):
    """
    Override CharField to convert to lowercase before saving.
    """

    def to_python(self, value):
        """
        Convert text to lowercase.
        """
        value = super(LowercaseCharField, self).to_python(value)
        # Value can be None so check that it's a string before lowercasing.
        if isinstance(value, str):
            return value.lower()
        return value


class User(AbstractUser):
    """
    Users, within the ChafPozi authentication system, are represented by this
    model.
    """
    object_id = models.CharField(max_length=20, null=True, blank=True)
    is_fake_profile = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    gelt = models.IntegerField(default=500)
    num_posts = models.PositiveIntegerField(default=0)
    username = LowercaseCharField(
        # Copying this from AbstractUser code
        _("username"),
        max_length=300,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        # validators=[
        #     UnicodeEmailValidator(),
        # ],
        error_messages={
            "unique": _("This username is not available, please try another one."),
        },
    )
    display_name = models.CharField(max_length=100, null=True, blank=True)
    profile_pic = ProcessedImageField(
        upload_to="accounts/profile_pics/",
        processors=[ResizeToFit(320, 440)],
        format="JPEG",
        options={"quality": 90},
        null=True,
        blank=True,
    )
    bio = models.TextField(null=True, blank=True, max_length=300)
    subscribers = models.PositiveBigIntegerField(default=1)
    upvotes = models.PositiveBigIntegerField(default=0)
    # User social media links
    instagram = models.CharField(max_length=60, null=True, blank=True)
    vsco = models.CharField(max_length=60, null=True, blank=True)
    twitter = models.CharField(max_length=60, null=True, blank=True)
    website = models.URLField(max_length=300, null=True, blank=True)

    # custom html
    default_html = models.TextField(null=False, blank=False, default="""
<style>
    /*
        Main Foxstraat user profile Stylesheet
        (c) 2020-2021 Samkelo Rocks (Pty) Ltd
    */

    :root {
        font-size: .8em;
    }

    *,
    *::before,
    *::after {
        box-sizing: border-box;
    }

    body {
        font-family: "Open Sans", Arial, sans-serif;
        min-height: 100vh;
        background-color: #fafafa;
        color: #000;
        padding-bottom: 3rem;
    }

    img {
        display: block;
    }

    .container {
        max-width: 93.5rem;
        margin: 0 auto;
        padding: 0 2rem;
    }

    .btn {
        display: inline-block;
        font: inherit;
        background: none;
        border: none;
        color: inherit;
        padding: 0;
        cursor: pointer;
    }

    /* Profile Section */
    .profile {
        padding: 5rem 0;
    }

    .profile::after {
        content: "";
        display: block;
        clear: both;
    }

    .profile-image {
        float: left;
        width: calc(33.333% - 1rem);
        display: flex;
        justify-content: center;
        align-items: center;
        margin-right: 3rem;
    }

    .profile-image img {
        border-radius: 50%;
    }

    .profile-user-settings {
        margin-top: 1.1rem;
    }

    .profile-user-name {
        display: inline-block;
        font-size: 2rem;
        font-weight: 300;
    }

    .profile-btn {
        text-decoration: none;
        font-size: 1.4rem;
        line-height: 1.8;
        border: 0.1rem solid #dbdbdb;
        border-radius: 0.3rem;
        padding: 0 2.4rem;
        margin-left: 2rem;
    }

    .profile-settings-btn {
        font-size: 2rem;
        margin-left: 1rem;
    }

    .profile-stats {
        margin-top: 2.3rem;
    }

    .profile-stats li {
        display: inline-block;
        font-size: 1.6rem;
        line-height: 1.5;
        margin-right: 4rem;
        cursor: pointer;
    }

    .profile-stats li:last-of-type {
        margin-right: 0;
    }

    .profile-bio {
        font-size: 1.6rem;
        font-weight: 400;
        line-height: 1.5;
        margin-top: 2.3rem;
    }

    .profile-real-name,
    .profile-stat-count,
    .profile-btn {
        font-weight: 600;
    }

    /* Gallery Section */

    .gallery {
        display: flex;
        flex-wrap: wrap;
        margin: -1rem -1rem;
        padding-bottom: 3rem;
    }

    .gallery-item {
        position: relative;
        flex: 1 0 22rem;
        margin: 1rem;
        color: #fff;
        cursor: pointer;
    }
    .gallery-item-link {
        color: #fff;
        text-decoration: none;
    }

    .gallery-item:hover .gallery-item-info,
    .gallery-item:focus .gallery-item-info {
        display: flex;
        justify-content: center;
        align-items: center;
        position: absolute;
        top: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.7);
    }

    .gallery-item-info {
        display: none;
    }

    .gallery-item-info li {
        display: inline-block;
        font-size: 1.7rem;
        font-weight: 600;
    }

    .gallery-item-likes {
        margin-right: 2.2rem;
    }

    .gallery-item-type {
        position: absolute;
        top: 1rem;
        right: 1rem;
        font-size: 2.5rem;
        text-shadow: 0.2rem 0.2rem 0.2rem rgba(0, 0, 0, 0.1);
    }

    .fa-clone,
    .fa-comment {
        transform: rotateY(180deg);
    }

    .gallery-image {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    @supports (display: grid) {
        .profile {
            display: grid;
            grid-template-columns: 1fr 2fr;
            grid-template-rows: repeat(3, auto);
            grid-column-gap: 3rem;
            align-items: center;
        }

        .profile-image {
            grid-row: 1 / -1;
        }

        .gallery {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(22rem, 1fr));
            grid-gap: 2rem;
        }

        .profile-image,
        .profile-user-settings,
        .profile-stats,
        .profile-bio,
        .gallery-item,
        .gallery {
            width: auto;
            margin: 0;
        }

        @media (max-width: 40rem) {
            .profile {
                grid-template-columns: auto 1fr;
                grid-row-gap: 1.5rem;
            }

            .profile-image {
                grid-row: 1 / 2;
            }

            .profile-user-settings {
                display: grid;
                grid-template-columns: auto 1fr;
                grid-gap: 1rem;
            }

            .profile-btn,
            .profile-stats,
            .profile-bio {
                grid-column: 1 / -1;
            }

            .profile-user-settings,
            .profile-btn,
            .profile-settings-btn,
            .profile-bio,
            .profile-stats {
                margin: 0;
            }
        }
    }
</style>
    """)
    custom_html = models.TextField(null=True, blank=True)

    date_joined = models.DateField(auto_now_add=True)
    datetime_joined = models.DateTimeField(auto_now_add=True)
