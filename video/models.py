from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    pass

class Sharer(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    sharer_name = models.CharField(max_length=120)
    shared_song_id = models.IntegerField()


class Comments(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    commenter = models.CharField(max_length=120)
    comment = models.CharField(max_length=500)
    commented_video_id = models.IntegerField()
    date_and_time = models.DateTimeField()

    def serialize(self):
        return{
            "id": self.id,
            "commenter": self.commenter,
            "comment": self.comment,
            "commented_video_id": self.commented_video_id,
            "date_and_time": self.date_and_time
        }


class Likes(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    liker = models.CharField(max_length=120)
    liked_video_id = models.IntegerField()

    def serialize(self):
        return{
            "id": self.id,
            "liker": self.liker,
            "liked_video_id": self.liked_video_id
        }


class Video(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    title = models.CharField(max_length=50, blank=False)
    mood = models.CharField(max_length=120, blank=True)
    posted_by = models.CharField(max_length=120, blank=False)
    video_link = models.CharField(max_length=300, blank=False)
    date_and_time = models.DateTimeField()

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "mood": self.mood,
            "posted_by": self.posted_by,
            "video_link": self.video_link,
            "date_and_time": self.date_and_time
        }
