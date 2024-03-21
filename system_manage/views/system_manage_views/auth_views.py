from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View, TemplateView
from django.http import HttpRequest, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib.auth.models import User

# Create your views here.
class HomeView(LoginRequiredMixin, TemplateView):
    '''
        관리자 메인 화면
    '''
    login_url='system_manage:login'
    template_name = 'system_manage/admin_main.html'
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}

        return render(request, self.template_name, context)

class LoginView(View):
    '''
        관리자 로그인 기능
    '''
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}
        if request.user.is_authenticated:
            return redirect('system_manage:home')
        
        return render(request, 'system_manage/admin_login.html', context)

    def post(self, request: HttpRequest, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            return JsonResponse({'message':'일치하는 회원정보가 없습니다'}, status = 400)
        
        user = authenticate(username=user.username, password=password)
        
        if user is not None:
            if user.is_superuser:
                login(request, user)
                if 'next' in request.GET:
                    url = request.GET.get('next')
                    url = url.split('?next=')[-1]
                else:
                    url = reverse('system_manage:home')
                return JsonResponse({'message':'로그인 되었습니다.', 'url':url}, status = 200)
            else:
                return JsonResponse({'message':'관리자가 아닙니다.'}, status = 400)
        else:
            return JsonResponse({'message':'일치하는 회원정보가 없습니다'}, status = 400)

class PermissionDeniedView(LoginRequiredMixin, TemplateView):
    login_url = 'system_manage:login'
    template_name='system_manage/permission_denied.html'


class NotFoundView(LoginRequiredMixin, TemplateView):
    login_url = 'system_manage:login'
    template_name='system_manage/not_found.html'


