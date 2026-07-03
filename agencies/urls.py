from django.urls import path
from . import views

app_name = "agencies"

urlpatterns = [
    path('agent/' , views.CreateAgencyView.as_view(), name='create-agency'),
]