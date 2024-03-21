from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import redirect


class State(models.Model):
    name = models.CharField(max_length=50, verbose_name='이름')
    alpha_code = models.CharField(max_length=10, verbose_name='알파벳 코드', unique=True)

    class Meta:
        db_table='state'

#문자인증
class SMSCertification(models.Model):
    phone = models.CharField(max_length=30, verbose_name='전화번호')
    certification_number = models.CharField(max_length=10, verbose_name='인증번호')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')

    class Meta:
        db_table='sms_certification'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    membername = models.CharField(null=True, max_length=50, verbose_name='회원명')
    phone = models.CharField(unique=True, max_length=30, verbose_name='전화번호')
    gender = models.CharField(default='M', max_length=10, verbose_name='성별') # M / F
    birth = models.DateField(null=True, verbose_name='생년월일')

    state = models.ForeignKey(State, on_delete=models.PROTECT, null=True)
    city = models.CharField(null=True, max_length=30, verbose_name='도시')
    zipcode = models.CharField(null=True, max_length=10, verbose_name='우편번호')
    oauth_type = models.CharField(default=None, max_length=20, verbose_name='oauth type') # google, facebook
    withdrawal_at = models.DateTimeField(null=True, verbose_name='탈퇴일')
    email_verified = models.BooleanField(default=False, verbose_name='이메일 인증여부')

    point = models.PositiveIntegerField(default=0, verbose_name='사용자 포인트')

    class Meta:
        db_table='auth_profile'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, oauth_type='')

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


def my_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return 'user_main.html'
        else:
            return HttpResponse("Invalid login details.")
        
def my_logout_view(request):
    logout(request)
    return 'user_login.html'

class Partner(models.Model):
    name = models.CharField(max_length=100)

class PaymentRecord(models.Model):
    date = models.DateField()
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE)
    beginning_balance = models.DecimalField(max_digits=10, decimal_places=2)
    claim = models.DecimalField(max_digits=10, decimal_places=2)
    ending_balance = models.DecimalField(max_digits=10, decimal_places=2)
    paid_claim = models.DecimalField(max_digits=10, decimal_places=2)
    claim_balance = models.DecimalField(max_digits=10, decimal_places=2)
    
