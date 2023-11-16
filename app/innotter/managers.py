from django.db import models
from django.core.exceptions import ObjectDoesNotExist

class FollowerManager(models.Manager):
    def follow_page(self, page, user_id):
        result = None
        try:
            self.get(page=page, user_id=user_id)
            result = False 
        except ObjectDoesNotExist:
            self.create(page=page, user_id=user_id)
            result = True
        return result

    def unfollow_page(self, page, user_id):
        result = None
        try:
            follower = self.get(page=page, user_id=user_id)
            follower.delete()
            result = True 
        except ObjectDoesNotExist:
            result = False
        return result
    
class LikeManager(models.Manager):
    def like_post(self, post, user_id):
        result = None
        try:
            self.get(post=post, user_id=user_id)
            result = False 
        except ObjectDoesNotExist:
            self.create(post=post, user_id=user_id)
            result = True
        return result

    def remove_like_post(self, post, user_id):
        result = None
        try:
            like = self.get(post=post, user_id=user_id)
            like.delete()
            result = True 
        except ObjectDoesNotExist:
            result = False
        return result