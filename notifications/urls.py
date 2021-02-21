from django.urls import path
from notifications.views import show_notifications,delete_notification

urlpatterns = [
    path('',show_notifications,name='show-notifications'),
    path('<noti_id>/delete',delete_notification,name='delete-notification'),
]
