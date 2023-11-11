from django.db import models
from django.dispatch import receiver

class Tag(models.Model):
    name = models.CharField(max_length=50)

class Page(models.Model):
    name = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=100, default=None, blank=True, null=True)
    user_id = models.UUIDField(null=False)
    image_url = models.URLField(default=None, blank=True, null=True)
    tags = models.ManyToManyField(Tag)
    followers = models.PositiveIntegerField(default=0)
    blocked = models.BooleanField(default=False)
    unblock_date = models.DateField(default=None, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class Post(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    content = models.JSONField()
    reply_to_post_id = models.PositiveBigIntegerField(default=None, blank=True, null=True)
    likes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class Follower(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    user_id = models.UUIDField(null=False)


class Like(models.Model):
    post =  models.ForeignKey(Post, on_delete=models.CASCADE)
    user_id = models.UUIDField(null=False)


@receiver(models.signals.post_save, sender=Like)
def update_post_likes(sender, instance, **kwargs):
    post = instance.post
    post.likes = Like.objects.filter(post=post).count()
    post.save()


@receiver(models.signals.post_save, sender=Follower)
def update_post_likes(sender, instance, **kwargs):
    page = instance.page
    page.followers = Follower.objects.filter(page=page).count()
    page.save()