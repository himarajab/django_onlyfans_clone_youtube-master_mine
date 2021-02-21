from notifications.models import Notification
from django.shortcuts import render,redirect

def show_notifications(request):
  user = request.user 
  notifications = Notification.objects.filter(user=user).order_by('-date')

  # after read notifications update the seen field
  Notification.objects.filter(user=user,is_seen=False).update(is_seen=True)


  context = {
    'notifications':notifications,
  }

  return render(request,'notifications.html',context)
  

def delete_notification(request,noti_id):
  user = request.user

  Notification.objects.filter(id=noti_id,user=user).delete()

  return redirect('show-notifications')


def count_notifications(request):
  count_notifications = None

  if request.user.is_authenticated:
    count_notifications = Notification.objects.filter(user=request.user,is_seen=False).count()
  return {'count_notifications':count_notifications}

