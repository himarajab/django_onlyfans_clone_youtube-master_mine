from notifications.models import Notification
from django import dispatch
from django.dispatch import receiver
from django.db.models.signals import post_save,post_delete
from django.db.models.sql import subqueries
from django.urls import reverse
import uuid
from tier.models import Tier,Subscription
from django.db import models
from django.contrib.auth.models import User

def user_directory_path(instance,file_name):
  # files will be uploaded to MEDIA_ROOT/the user(id)/the file
  user_id = instance.user.id
  return f'user_{user_id}/{file_name}'


# to enable user to upload multible images in one post
class PostFileContent(models.Model):
    user = models.ForeignKey(User, related_name=("content_owner"), on_delete=models.CASCADE)
    file= models.FileField(upload_to=user_directory_path, max_length=100)
    tier = models.ForeignKey(Tier, related_name=("tier_file"), on_delete=models.CASCADE)
    posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
      return str(self.file)
  

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.ManyToManyField(PostFileContent, verbose_name=("contents"))
    title = models.CharField(max_length=150)
    caption = models.TextField(max_length=1500,verbose_name='Caption')
    posted = models.DateTimeField(auto_now_add=True)
    tier = models.ForeignKey(Tier, related_name=("tiers"), on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    favorites_count = models.IntegerField(default=0)

    def get_absolute_url(self):
        # the url user will get when click on the post
        return reverse("post-detail", args=str(self.id))
    def __str__(self) -> str:
        return f'{self.title}'   

# to show posts from user u subscribe to them 

class Stream(models.Model):
    # the persons subscibe to the current user 
    subscribed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stream_subscribed')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    visible = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return f'{self.user} subscribe to {self.subscribed}'


    # notify useres when people they foloow create posts
    # prevent double signal fire (tow posts)
    @receiver(post_save, sender=Post, dispatch_uid='unique_add_post')
    def add_post(sender, instance, created, **kwargs):
        post = instance
        user = post.user

        if created:
            subscribers = Subscription.objects.all().filter(subscribed=user)
            for subscriber in subscribers:
                if(subscriber.tier.number >= post.tier.number):
                    stream = Stream(post=post, user=subscriber.subscriber, date=post.posted, subscribed=user, visible=True)
                    stream.save()
                else:
                    stream = Stream(post=post, user=subscriber.subscriber, date=post.posted, subscribed=user)
                    stream.save()


                    


class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')

    def user_liked_post(sender, instance, *args, **kwargs):
        like = instance
        post = like.post
        sender = like.user

        notify = Notification(post=post,sender=sender,user=post.user,notification_type=1)
        notify.save()

    # cause if user change his mind we remove the Notification
    def user_unlike_post(sender,instance,*args, **kwargs):
        like = instance
        post = like.post
        sender = like.user

        notify = Notification.objects.filter(post=post,sender=sender,notification_type=1)
        notify.delete()


class Bookmark(models.Model):
    posts = models.ManyToManyField(Post)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmark_user')


    def __str__(self) -> str:
        return f'{self.user} {self.posts}'


# signal stuff for likes 
post_save.connect(Likes.user_liked_post,sender=Likes)
post_delete.connect(Likes.user_unlike_post,sender=Likes)