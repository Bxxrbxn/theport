from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned
from django.core.validators import RegexValidator
from django.db import transaction
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from website.tokens import account_activation_token
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from system_manage.models import State
from validate_email import validate_email
import datetime, random, traceback

from system_manage.models import Profile, SMSCertification

from api.serializers.auth_serializers import RegistrationSerializer, EmailSerializer, PhoneSerializer, CertificationNumberSerializer, FindEmailSerializer

class RegistrationView(GenericAPIView):
    '''
        회원 가입 API
    '''
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            first_name = serializer.validated_data['first_name']
            last_name = serializer.validated_data['last_name']
            gender = serializer.validated_data['gender']
            birth = serializer.validated_data['birth']
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            phone = serializer.validated_data['phone']
            city = serializer.validated_data['city']
            state = serializer.validated_data['state']
            zipcode = serializer.validated_data['zipcode']

            if not validate_password(password):
                return Response({
                    "message": "비밀번호는 숫자와 영문자 조합으로 8~16자리를 사용해야 합니다."}, 
                    status=status.HTTP_400_BAD_REQUEST)
            if not validate_email(email):
                return Response({"message": "유효하지 않은 이메일 주소입니다."},
                    status=status.HTTP_400_BAD_REQUEST)
            if not validate_phone(phone):
                return Response({
                    "message": "유효하지 않은 전화번호 형식입니다."},
                    status=status.HTTP_400_BAD_REQUEST)
            try:
                User.objects.get(email=email)
                return Response({
                    "message": "이미 가입하신 이메일 입니다."},
                    status=status.HTTP_400_BAD_REQUEST)
            except:
                pass
            try:
                Profile.objects.get(phone=phone)
                return Response({
                    "message": "이미 가입하신 전화번호 입니다."},
                    status=status.HTTP_400_BAD_REQUEST)            
            except MultipleObjectsReturned:
                return Response({
                    "message": "가입된 번호가 여러개 있습니다. 관리자에게 문의하세요."},
                    status=status.HTTP_400_BAD_REQUEST)   
            except:
                pass
            try:
                state_obj = State.objects.get(alpha_code = state)
            except:
                return Response({
                    "message" : "옳지 않은 주소입니다."},
                    status=status.HTTP_400_BAD_REQUEST
                    )

            try:
                with transaction.atomic(): 
                    user = User.objects.create_user(
                        username=email,
                        email=email,
                        password=password
                    )
                    user.first_name = first_name
                    user.last_name = last_name
                    user.is_active = False
                    user.profile.gender = gender
                    user.profile.birth = birth
                    user.profile.phone = phone
                    user.profile.city = city
                    user.profile.state = state_obj
                    user.profile.zipcode = zipcode
                    user.profile.point = 0
                    user.profile.email_verified = False
                    user.save()
                        

                current_site = get_current_site(request) 
                message = render_to_string('authentication/activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                mail_title = "Email Authentication"
                sendEmail = EmailMessage(mail_title, message, settings.EMAIL_HOST_USER, to=[email])
                sendEmail.send()
                    
            except Exception as e:
                print(e)
                return Response({"message": "가입 오류 발생."}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"url":reverse('website:activation_confirm') + f'?email={email}'},
                status=status.HTTP_201_CREATED)



class ValidateEmailView(GenericAPIView):
    '''
        이메일 유효 체크 API
    '''
    permission_classes = [AllowAny]
    serializer_class = EmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data['email']
            if not validate_email(email):
                return Response({"message": "유효하지 않은 이메일 주소입니다."},
                status=status.HTTP_400_BAD_REQUEST)
            try:
                User.objects.get(email=email)
                return Response({"message": "이미 가입한 이메일 입니다."},
                status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response(
                    {"message": "사용가능한 이메일 입니다.", "email":email},
                    status=status.HTTP_200_OK)


class CertificatePhoneView(GenericAPIView):
    '''
        휴대폰 문자 인증 API
    '''
    permission_classes = [AllowAny]
    serializer_class = PhoneSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            phone = serializer.validated_data['phone']
            if not validate_phone(phone):
                return Response({
                    "message": "유효하지 않은 전화번호 형식입니다."},
                    status=status.HTTP_400_BAD_REQUEST)
            if Profile.objects.filter(phone=phone).exists():
                return Response({
                    "message": "이미 가입하신 전화번호 입니다."},
                    status=status.HTTP_400_BAD_REQUEST)

            MAX_SMS_SECONDS = 180
            expiry_date = timezone.now() - datetime.timedelta(seconds=MAX_SMS_SECONDS)
            SMSCertification.objects.filter(created_at__lte=expiry_date).delete()
            certification_history = SMSCertification.objects.filter(phone=phone).order_by('created_at')
            if certification_history.count() >= 5:
                remaining_time = certification_history.first().created_at + datetime.timedelta(seconds=MAX_SMS_SECONDS) - timezone.now()
                return Response({
                    "message": f"재요청 횟수를 초과했습니다. {remaining_time.seconds}초 후에 후 다시 시도해주세요."},
                    status=status.HTTP_400_BAD_REQUEST)
            
            # certification_number = random.randint(100000, 1000000)
            certification_number = '000000'
            try:
                with transaction.atomic():
                    SMSCertification.objects.create(
                        phone=phone,
                        certification_number=certification_number,
                    )
            except:
                return Response({"message": "문자 전송 실패"},
                status=status.HTTP_400_BAD_REQUEST)
            
            return Response({"message": "문자가 전송되었습니다. 인증번호를 확인해주세요."},
                status=status.HTTP_201_CREATED)

class ValidateSMSCertificationNumberView(GenericAPIView):
    '''
        인증번호 확인 API
    '''
    permission_classes = [AllowAny]
    serializer_class = CertificationNumberSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            phone = serializer.validated_data['phone']
            certification_number = serializer.validated_data['certification_number']

            MAX_SMS_SECONDS = 180
            expiry_date = timezone.now() - datetime.timedelta(seconds=MAX_SMS_SECONDS)
            history = SMSCertification.objects.filter(phone=phone, created_at__gte=expiry_date).order_by('-created_at')
            if history.exists():
                if history.first().certification_number == certification_number:
                    return Response({"message": "Certified.", "phone" : phone},
                    status=status.HTTP_200_OK)
                else:
                    return Response({"message": "Verification number does not match."},
                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "Authentication request time expired"},
                status=status.HTTP_400_BAD_REQUEST)


class GetStateView(GenericAPIView):
    '''
        미국 주 조회 API
    ''' 
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        state = State.objects.all("name")
        return Response(state, status=status.HTTP_200_OK)


class FindEmailView(GenericAPIView):
    '''
        아이디 찾기 API
    '''
    permission_classes = [AllowAny]
    serializer_class = FindEmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            first_name = serializer.validated_data['first_name']
            last_name = serializer.validated_data['last_name']
            phone = serializer.validated_data['phone']

            try:
                profile = Profile.objects.get(phone=phone, user__first_name = first_name, user__last_name = last_name, oauth_type='')
            except:
                return Response({"message": "일치하는 회원이 없습니다."},
                                status=status.HTTP_400_BAD_REQUEST)

            return Response({"email": profile.user.email},
                            status=status.HTTP_200_OK)


def validate_password(password):
    '''
    비밀번호 유효성 체크
    '''
    try:
        RegexValidator(regex=r'^[a-zA-z0-9!@#$%^&*()+.,~]{8,16}$')(password)
    except:
        return False

    return True

def validate_phone(phone):
    '''
    전화번호 유효성 체크
    '''
    try:
        RegexValidator(regex=r'^(1\s?)?(\(\d{3}\)|\d{3})[\s\-]?\d{3}[\s\-]?\d{4}$')(phone)
    except:
        return False

    return True