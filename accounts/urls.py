from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import MyTokenObtainPairView, UserView

app_name = "accounts_app"

urlpatterns = [
    path("register/", UserView.as_view(), name="register"),
    path("login/", MyTokenObtainPairView.as_view(), name="login"),
    path("refresh/", jwt_views.TokenRefreshView.as_view(), name="token-refresh"),
]
