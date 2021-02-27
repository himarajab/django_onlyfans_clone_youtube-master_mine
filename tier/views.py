from datetime import datetime,timedelta, tzinfo
from django.contrib.auth.models import User
from tier.models import Tier,Subscription
from django.shortcuts import get_list_or_404, render,redirect,get_object_or_404,HttpResponse
from tier.forms import NewTierForm

def new_tier(request):
  user = request.user
  if request.method == 'POST':
    form = NewTierForm(request.POST)
    if form.is_valid():
      description = form.cleaned_data.get('description')
      price = form.cleaned_data.get('price')
      can_message = form.cleaned_data.get('can_message')

      Tier.objects.create(description=description,price=price,user=user,can_message=can_message)

      return redirect('index')
  else:
    form = NewTierForm()
  context = {'form':form,}
  return render(request,'new_tier.html',context)

# subscribe based on tier level
def subscribe(request,username,tier_id):
  user = request.user
  subscribing = get_object_or_404(User, username=username)
  tier = Tier.objects.get(id=tier_id)

  try:
      subscribed = Subscription.objects.get_or_create(subscriber=user, subscribed=subscribing, tier=tier)
      return redirect('index')
  except User.DoesNotExist:
      return HttpResponse(f'{user} does not exist')

def fans_list(request):
  # people subscribed to u
  my_fans = Subscription.objects.filter(subscribed=request.user)
  context = {
    'my_fans':my_fans,
    }
  return render(request,'fans_list.html',context)


def following_list(request):
  # people u ar follow
  my_follows = Subscription.objects.filter(subscriber=request.user)
  
  # each subscriation is for one month and will display how days remaining for the expiration date 
  for follows in my_follows:
    if follows.expired !=True:
      end_date = datetime.now() - timedelta(days=6)
      # calculate the date and drop the time zone info 
      remaining = follows.date.replace(tzinfo=None) - end_date.replace(tzinfo=None)
      days_left = remaining.days
      follows.date = days_left


  context = {
    'my_follows':my_follows,
    }
  return render(request,'following_list.html',context)

def check_expiration(request):
  exp_date = datetime.now() - timedelta(days=6)
  subs = Subscription.objects.filter(subscriber=request.user,date__lt=exp_date)
  subs.update(expired=True)
  fans = Subscription.objects.filter(subscribed=request.user,date__lt=exp_date)
  fans.update(expired=True)

  return redirect('index')