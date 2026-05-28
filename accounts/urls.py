from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path('user/send/code/' , views.SendOtpView.as_view(), name='send-otp'),
]