from django.urls import path
from .views import register_view, login_view, home_view, UserDetailView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('home/', home_view, name='home'),
    path('user/<str:username>/', UserDetailView.as_view(), name='user_detail'),
]
