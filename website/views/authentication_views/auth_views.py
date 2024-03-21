from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View, TemplateView
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from website.tokens import account_activation_token
from rest_framework.response import Response
from rest_framework import status
from system_manage.models import State
import json

# Create your views here.
class HomeView(TemplateView):
    '''
        사용자 메인 화면
    '''
    template_name = 'authentication/user_main.html'
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}

        return render(request, self.template_name, context)

class LoginView(View):
    '''
        사용자 로그인
        김혜원 2024.01.26
    '''
    def get(self, request:HttpRequest, *args, **kwargs):
        context= {}
        if request.user.is_authenticated:
            return redirect('website:home')
        return render(request, 'authentication/user_login.html', context)
    
    def post(self, request:HttpRequest, *args, **kwargs):
        context ={}
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(username=email, password=password)

        if user is not None:
            if user.profile.withdrawal_at:
                context["success"] = False
                context["message"] = "탈퇴한 사용자 입니다."
                return JsonResponse(context, content_type="application/json")
            login(request, user)
            if 'next' in request.GET:
                url = request.GET.get('next')
                context['url'] = url.split('?next=')[-1]
            else:
                context['url'] = reverse('website:home')

            context['success'] = True
            context['message'] = '로그인 되었습니다.'
            return JsonResponse(context, content_type='application/json', status=status.HTTP_200_OK)

        else:
            context['success'] = False
            context['message'] = '일치하는 회원정보가 없습니다.'
        return JsonResponse(context, content_type='application/json', status=status.HTTP_400_BAD_REQUEST)


class RegistrationView(View):
    '''
        사용자 회원가입
        김혜원 2024.01.26
    '''
    def post(self, request:HttpRequest, *args, **kwargs):
        context = {}
        if request.user.is_authenticated:
            return redirect('website:home')
        phone = request.POST.get("phone")
        state = State.objects.all().order_by("name")
        context["state"] = state
        context['phone'] = phone
        return render(request, 'authentication/user_registration.html', context)


class CertificatePhoneView(View):
    '''
        사용자 문자 인증
        김혜원 2024.01.26
    '''
    def get(self, request:HttpRequest, *args, **kwargs):
        context= {}
        if request.user.is_authenticated:
            return redirect('website:home')        
        return render(request, "authentication/user_certificate_phone.html", context)


class ActivationConfirmView(View):
    '''
        이메일 보냄 확인 페이지
    '''
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}
        email = request.GET.get('email', '')
        context['email'] = email

        return render(request, 'authentication/activation_confirm.html', context)


class FindEmailView(View):
    '''
        사용자 이메일 찾기
        김혜원 2024.01.30
    '''
    def get(self, request:HttpRequest, *args, **kwargs):
        context= {}
        if request.user.is_authenticated:
            return redirect('website:home')
        return render(request, "authentication/user_find_email.html", context)


def activate(request: HttpRequest, uidb64, token):
    '''
        토큰 인증을 통한 계정 활성화
    '''
    if request.method=='GET':
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return render(request, 'authentication/activation_complete.html', {'username' : user.username})
        else:
            return render(request, 'authentication/activation_error.html', {'error' : '만료 된 링크입니다.'})