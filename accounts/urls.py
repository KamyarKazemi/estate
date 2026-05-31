from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path('user/register/send/code/' , views.SendOtpRegisterView.as_view(), name='register-send-code'),
    path('user/register/verify/code/' , views.VerifyOtpRegisterView.as_view(), name='register-verify-code'),
    path('user/complete/register/' , views.CompleteRegisterView.as_view(), name='complete-register'),
    path('user/login/send/code/' , views.SendOtpLoginView.as_view(), name='login-send-code'),
    path('user/login/verify/code/' , views.VerifyOtpLoginView.as_view(), name='login-verify-code'),
]