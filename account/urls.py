from django.urls import path
from .views import LoginUserView, LogoutApiView

from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('auth/login/', LoginUserView.as_view(), name='login-user'),
    path('auth/logout/', LogoutApiView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]