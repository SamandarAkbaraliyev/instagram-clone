from django.db import models
from utils.models import BaseModel


class Location(BaseModel):
    name = models.CharField(max_length=256)


class Post(BaseModel):
    author = models.ManyToManyField('users.User', related_name='posts')

    caption = models.TextField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='posts')

    likes = models.ManyToManyField('users.User', related_name='likes')

    is_deleted = models.BooleanField(default=False)


class File(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='post/')


class Comment(BaseModel):
    author = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children')
