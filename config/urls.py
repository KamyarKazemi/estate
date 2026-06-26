from django.contrib import admin
from django.urls import path , include
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('accounts/' , include('accounts.urls' , namespace='accounts')),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/",SpectacularSwaggerView.as_view(url_name="schema"),name="swagger-ui",),
]
