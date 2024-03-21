from django.urls import path, include
#APP
from api.views.authentication_views.auth_views import RegistrationView, ValidateEmailView, CertificatePhoneView, ValidateSMSCertificationNumberView, FindEmailView

app_name='api'
urlpatterns = [
    path('registration/', RegistrationView.as_view()),
    path('validate-email/', ValidateEmailView.as_view()),
    path('certificate-phone/', CertificatePhoneView.as_view()),
    path('validate-sms-certification-number/', ValidateSMSCertificationNumberView.as_view()),
    path('find-email/', FindEmailView.as_view()),
]