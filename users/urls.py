from django.urls import path, re_path
from .views import (
    CustomProviderAuthView,
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    CustomTokenVerifyView, 
    LogouttView
)

urlpatterns = [
    re_path(r'^o/(?P<provider>\S+)/$', CustomProviderAuthView.as_view(), name='google'),
    path('jwt/create/', CustomTokenObtainPairView.as_view(), name='create'),
    path('jwt/refresh/', CustomTokenRefreshView.as_view(), name='refresh'),
    path('jwt/verify/', CustomTokenVerifyView.as_view(), name='verify'),
    path('jwt/logout/', LogouttView.as_view(), name='logout'),
]
