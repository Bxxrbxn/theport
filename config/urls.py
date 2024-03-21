from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls')),
    path('api/', include('api.urls')),
    path('system-manage/', include('system_manage.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
