from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "content": self.content,
            "timestamp": self.created_at,
            "likes": self.like_count(),
        }

    def like_count(self):
        return self.likes.count()

    def is_liked(self, user):
        return user in self.likes.all()


class Follow(models.Model):
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following"
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followers"
    )
