from django.urls import path
from tier.views import new_tier,fans_list,following_list,check_expiration

urlpatterns = [
    path('new_tier',new_tier,name='new-tier'),
    path('myfans',fans_list,name='myfans'),
    path('myfollows',following_list,name='myfollows'),
    path('checkexpiration',check_expiration,name='check-expiration'),
]
