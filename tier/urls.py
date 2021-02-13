from django.urls import path
from tier.views import new_tier

urlpatterns = [
    path('new_tier',new_tier,name='new-tier'),
]
