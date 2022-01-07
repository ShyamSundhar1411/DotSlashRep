import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from autoslug import AutoSlugField
# Create your models here.
class ToDo(models.Model):
    title = models.CharField(max_length = 200)
    memo = models.TextField(max_length = 200)
    isImportant = models.BooleanField(default = False)
    isCompleted = models.BooleanField(default = False)
    created = models.DateTimeField(auto_now_add = True)
    slug = AutoSlugField(populate_from = "title",unique = True,blank = True,editable = True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.title
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    avatar = models.ImageField(upload_to = "avatar/",blank = True)
    slug = models.SlugField(blank = True,unique = True)
    def __str__(self):
        return self.user.username
    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = uuid.uuid4()
        super(Profile,self).save(*args,**kwargs)
@receiver(post_save,sender = User)
def create_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user = instance)
        instance.profile.save()
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()