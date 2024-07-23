from django.db import models
from storages.backends.gcloud import GoogleCloudStorage
from django.contrib.auth.models import User

from django.dispatch import receiver
from django.db.models.signals import post_save

from UsersAuth.settings import GOOGLE_CLOUD_STORAGE_BASE

storage = GoogleCloudStorage()

class Upload:
    @staticmethod
    def upload_image(file, filename):
        try:
            target_path = 'profile-pictures/' + filename
            storage.save(target_path, file)
            return GOOGLE_CLOUD_STORAGE_BASE+"/"+target_path
        except Exception as e:
            print(f'Failed to upload: {e}')
            raise e


class UserProfile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=256, blank=True)
    picture = models.URLField(max_length=200, blank=True)


@receiver(post_save, sender=User)
def create_profile_for_new_user(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)   
        
        
class Follow(models.Model):
    followed = models.ForeignKey(User, related_name="followed", on_delete=models.CASCADE)
    follower = models.ForeignKey(User, related_name="follower", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

