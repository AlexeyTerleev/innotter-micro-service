from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from innotter.models import Like, Follower

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