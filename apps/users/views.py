from django.db.models import Q
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


User = get_user_model()

# Create your views here.


class CustomBackend(ModelBackend):
    '''自定义用户验证'''

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username)|Q(mobile=username))
            if user.check_password(password) and user.is_delete != True:
                return user
        except Exception as e:
            return None


# class SmsCodeViewSet(CreateModelMixin, viewsets.GenericViewSet):
#     '''发送短信验证码'''
#
#     serializer_class = SmsSerializer
#
#     def generate_code(self):
#         '''生成4位数验证码'''
#         seeds = '1234567890'
#         random_str = []
#         for i in range(4):
#             random_str.append(choice(seeds))
#
#         return ''.join(random_str)
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#
#         mobile = serializer.validated_data['mobile']
#         code = self.generate_code()
#         sms_status = yunpian.send_sms(code, mobile)
#         if sms_status['code'] != 0:
#             return Response({
#                 'mobile': sms_status['msg']
#             }, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             code_record = VerifyCode(code=code, mobile=mobile)
#             code_record.save()
#             return Response({
#                 'mobile': mobile,
#                 'code': code
#             }, status=status.HTTP_201_CREATED)