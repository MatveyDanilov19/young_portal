from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import register


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('news.urls', namespace='news')),
    path('profiles/', include('profiles.urls', namespace='profiles')),
    path('ratings/', include('ratings.urls', namespace='ratings')),
    path('accounts/register/', register, name='register'),  # Новый путь
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
