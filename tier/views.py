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
