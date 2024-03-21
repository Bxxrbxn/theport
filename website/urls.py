from django.urls.conf import path
from django.contrib.auth.views import LogoutView
from website.views.authentication_views.auth_views import HomeView
from website.views.authentication_views.auth_views import HomeView, LoginView, RegistrationView, CertificatePhoneView, FindEmailView, ActivationConfirmView, activate
from website.views.authentication_views.password_reset_views import UserPasswordResetView, UserPasswordResetDoneView, CustomPasswordResetConfirmView, UserPasswordResetCompleteView

app_name = 'website'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='website:home'), name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('certificate-phone/', CertificatePhoneView.as_view(), name='certificate_phone'),
    path('activation-confirm/', ActivationConfirmView.as_view(), name='activation_confirm'),
    path('activate/<str:uidb64>/<str:token>/', activate, name="activate"),
    path('find-email/', FindEmailView.as_view(), name='find_email'),

    path('password-reset/', UserPasswordResetView.as_view(), name='password_reset'),
    path('password-reset-done/', UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('password-reset-complete/', UserPasswordResetCompleteView.as_view(), name="password_reset_complete"),


]