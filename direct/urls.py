from django.urls import path
from direct.views import people_we_can_message,new_conversation,inbox,directs,send_direct

urlpatterns = [
    path('start/',people_we_can_message,name='people-we-can-message'),
    path('new/<username>',new_conversation,name='new-conversation'),
    path('directs/<username>',directs,name='directs'),
    path('send/',send_direct,name='send-direct'),
    path('',inbox,name='inbox'),
]
