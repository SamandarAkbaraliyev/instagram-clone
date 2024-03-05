from django.db import models
from utils.models import BaseModel
from django.utils import timezone
from celery import shared_task
from django.db.models.signals import post_save
from django.dispatch import receiver


class Story(BaseModel):
    author = models.ForeignKey('users.User', on_delete=models.CASCADE)

    file = models.FileField(upload_to='story/', null=True)
    caption = models.TextField()

    is_visible = models.BooleanField(default=True)


@receiver(post_save, sender=Story)
def schedule_visibility_change(sender, instance, created, **kwargs):
    if created:
        change_visibility.apply_async(args=[instance.id], countdown=24*60*60)


@shared_task
def change_visibility(story_id):
    try:
        story = Story.objects.get(pk=story_id)
        story.is_visible = False
        story.save()
    except Story.DoesNotExist:
        pass
