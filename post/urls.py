from django.urls import path
from post.views import new_post,post_details,like,BookmarkList,bookmark

urlpatterns = [
    path('new_post',new_post,name='new-post'),
    path('bookmarks',BookmarkList,name='bookmarks'),
    path('<uuid:post_id>',post_details, name='post-detail'),
    # path('<uuid:post_id>',post_details, name='post-detail'),
    path('<uuid:post_id>/like',like, name='postlike'),
    path('<uuid:post_id>/bookmark',bookmark, name='postbookmark'),

]
