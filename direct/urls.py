from django.urls import path
from direct.views import people_we_can_message,new_conversation,inbox,directs,send_direct,load_more,user_search

urlpatterns = [
    path('start/',people_we_can_message,name='people-we-can-message'),
    path('new/<username>',new_conversation,name='new-conversation'),
    path('directs/<username>',directs,name='directs'),
    path('send/',send_direct,name='send-direct'),
    path('loadmore/',load_more,name='load-more'),
    path('',inbox,name='inbox'),
    path('user_search',user_search,name='user-search'),
]
