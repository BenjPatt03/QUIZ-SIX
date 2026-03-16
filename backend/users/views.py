from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import MyTokenObtainPairSerializer, RegisterSerializer, UserSerializer
from .permissions import IsAdminRole

User = get_user_model()


class MyTokenObtainPairView(TokenObtainPairView):
	serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
	serializer_class = RegisterSerializer


class UserProfileView(generics.RetrieveAPIView):
	permission_classes = [permissions.IsAuthenticated]
	serializer_class = UserSerializer

	def get_object(self):
		return self.request.user


class AdminUserListView(generics.ListAPIView):
	permission_classes = [IsAdminRole]
	serializer_class = UserSerializer
	queryset = User.objects.all().order_by("id")


class AdminUserDetailView(generics.RetrieveUpdateDestroyAPIView):
	permission_classes = [IsAdminRole]
	serializer_class = UserSerializer
	queryset = User.objects.all().order_by("id")
