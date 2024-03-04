from urllib.parse import urlparse

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from utils.models import BaseModel


class Gender(models.TextChoices):
    MALE = 'Male'
    FEMALE = 'Female'
    NOT_SAY = 'Prefer not to say'


class User(AbstractUser):
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    bio = models.TextField(null=True)
    gender = models.CharField(max_length=64, choices=Gender.choices, default=Gender.NOT_SAY)

    following = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='follower_users')
    followers = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='following_users')

    muted_accounts = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='muting')
    close_friends = models.ManyToManyField('self', symmetrical=False, related_name='friends_of', blank=True)
    blocked_accounts = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='blocking')

    saved_posts = models.ForeignKey('post.Post', on_delete=models.CASCADE, null=True, blank=True)

    is_private = models.BooleanField(default=False)

    photo = models.ImageField(upload_to='profile/photos/', null=True)
    avatar = models.ImageField(upload_to='profile/avatars/', null=True)

    def get_absolute_url(self) -> str:
        return reverse("users:detail", kwargs={"username": self.username})


class WebsiteLink(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='links')
    name = models.CharField(max_length=256, null=True, blank=True)
    url = models.URLField(max_length=256)

    def save(self, *args, **kwargs):
        parsed_url = urlparse(self.url)
        self.name = parsed_url.netloc.split('.')[-2].capitalize()
        super().save()
