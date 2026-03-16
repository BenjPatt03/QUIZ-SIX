from rest_framework import generics, permissions

from .models import Service
from .serializers import ServiceSerializer


class ServiceListView(generics.ListAPIView):
	serializer_class = ServiceSerializer
	queryset = Service.objects.select_related("seller").order_by("-id")


class ServiceDetailView(generics.RetrieveAPIView):
	serializer_class = ServiceSerializer
	queryset = Service.objects.select_related("seller").all()


class SellerServiceManageView(generics.ListCreateAPIView):
	permission_classes = [permissions.IsAuthenticated]
	serializer_class = ServiceSerializer

	def get_queryset(self):
		return Service.objects.filter(seller=self.request.user).order_by("-id")

	def perform_create(self, serializer):
		serializer.save(seller=self.request.user)


class SellerServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
	permission_classes = [permissions.IsAuthenticated]
	serializer_class = ServiceSerializer

	def get_queryset(self):
		return Service.objects.filter(seller=self.request.user)
