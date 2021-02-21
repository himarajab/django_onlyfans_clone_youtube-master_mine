from post.views import index
from tier.views import subscribe
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from authy.views import UserProfile,remove_from_list


urlpatterns = [
    path('admin/', admin.site.urls),
    path('sub/', include('tier.urls')),
    path('user/', include('authy.urls')),
    path('post/', include('post.urls')),
    path('notifications/', include('notifications.urls')),
    # path('messages/', include('direct.urls')),
    path('', index, name='index'),
    path('<username>/', UserProfile, name='profile'),
    path('<username>/photos', UserProfile, name='profilephotos'),
    path('<username>/videos', UserProfile, name='profilevideos'),
    path('<username>/<tier_id>/subscribe', subscribe, name='subscribe'),
    path('<username>/remove/from_list', remove_from_list, name='remove-from-list'),

] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
