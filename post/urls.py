from django.urls import path
from post.views import new_post,post_details,like

urlpatterns = [
    path('new_post',new_post,name='new-post'),
    path('<uuid:post_id>',post_details, name='post-detail'),
    path('<uuid:post_id>/like',like, name='post-like'),

]
