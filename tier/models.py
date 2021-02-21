from notifications.models import Notification
from django.db import models
from django.db.models.signals import post_save,post_delete

from django.contrib.auth.models import User

class Tier(models.Model):
    number = models.PositiveSmallIntegerField(default=0)
    description = models.TextField(max_length=800,verbose_name='Description')
    price = models.IntegerField(verbose_name='Price')
    # define whether user can send direct message based on his tier
    can_message = models.BooleanField(default=False)
    user = models.ForeignKey(User, related_name=("tier_user"), on_delete=models.CASCADE)


    def __str__(self):
        return f'Tier {str(self.description)}'

    def save(self,*args, **kwargs):
        amount = Tier.objects.filter(user=self.user).count()
        self.number = amount+1
        return super().save(*args, **kwargs)

class Subscription(models.Model):
    subscriber = models.ForeignKey(User, related_name=("subscriber"), on_delete=models.CASCADE)
    subscribed = models.ForeignKey(User, related_name=("subscribed"), on_delete=models.CASCADE)
    tier = models.ForeignKey(Tier, related_name=("tier"), on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    expired = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.subscriber.username} == {self.subscribed.username} == Tier {self.tier.number}'

    
    def user_subscribed(sender, instance, *args, **kwargs):
        subscription = instance
        sender = subscription.subscriber
        # user receives the notification
        subscribing = subscription.subscribed


        notify = Notification(sender=sender,user=subscribing,notification_type=3)
        notify.save()

    # cause if user change his mind we remove the Notification
    def user_unsubscribed(sender,instance,*args, **kwargs):
        subscription = instance
        sender = subscription.subscriber
        # user receives the notification
        subscribing = subscription.subscribed

        notify = Notification.objects.filter(sender=sender,user=subscribing,notification_type=3)
        notify.delete()


# Subscription signals stuff 
post_save.connect(Subscription.user_subscribed,sender=Subscription)
post_delete.connect(Subscription.user_unsubscribed,sender=Subscription)