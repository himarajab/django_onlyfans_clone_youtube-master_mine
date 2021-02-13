from django.db import models

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
        # return f'{self.subscriber.username} == {self.subscriber.username} == Tier {self.tier.number}'
        return str(self.id)