from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    AdminUserDetailView,
    AdminUserListView,
    MyTokenObtainPairView,
    RegisterView,
    UserProfileView,
)

urlpatterns = [
    path("login/", MyTokenObtainPairView.as_view(), name="login"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("admin/users/", AdminUserListView.as_view(), name="admin_users"),
    path("admin/users/<int:pk>/", AdminUserDetailView.as_view(), name="admin_user_detail"),
]
