from django.urls.conf import path
from django.contrib.auth.views import LogoutView

from system_manage.views.system_manage_views.auth_views import HomeView, LoginView, PermissionDeniedView, NotFoundView

app_name = 'system_manage'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='system_manage:login'), name='logout'),
    path('denied/', PermissionDeniedView.as_view(), name='denied'),
    path('notfound/', NotFoundView.as_view(), name='notfound'),
]