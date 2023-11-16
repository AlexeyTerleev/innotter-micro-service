from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from innotter.models import Follower, Like


@receiver([post_save, post_delete], sender=Like)
def update_post_likes(sender, instance, **kwargs):
    post = instance.post
    post.likes = Like.objects.filter(post=post).count()
    post.save()


@receiver([post_save, post_delete], sender=Follower)
def update_page_follower(sender, instance, **kwargs):
    page = instance.page
    page.followers = Follower.objects.filter(page=page).count()
    page.save()
