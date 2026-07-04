from django.urls import path
from . import views

app_name = "agencies"

urlpatterns = [
    path('agent/' , views.CreateAgencyView.as_view(), name='create-agency'),
    path('agent/update/' , views.UpdateAgencyView.as_view(), name='update-agency'),
    path('detail/public/<int:pk>/' , views.AgencyPublicDetailView.as_view(), name='detail-public'),
]