from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import SellerApplication
from .serializers import SellerApplicationSerializer
from users.permissions import IsAdminRole

User = get_user_model()


class SubmitApplicationView(generics.CreateAPIView):
	permission_classes = [permissions.IsAuthenticated]
	serializer_class = SellerApplicationSerializer

	def create(self, request, *args, **kwargs):
		application, created = SellerApplication.objects.get_or_create(user=request.user)
		if not created and application.status == SellerApplication.Status.APPROVED:
			return Response({"detail": "Already approved"}, status=status.HTTP_400_BAD_REQUEST)
		application.status = SellerApplication.Status.PENDING
		application.decline_reason = None
		application.save()
		return Response(SellerApplicationSerializer(application).data, status=status.HTTP_201_CREATED)


class ListApplicationView(generics.ListAPIView):
	permission_classes = [IsAdminRole]
	serializer_class = SellerApplicationSerializer
	queryset = SellerApplication.objects.select_related("user").order_by("-created_at")


class ApproveApplicationView(generics.GenericAPIView):
	permission_classes = [IsAdminRole]
	serializer_class = SellerApplicationSerializer

	def post(self, request, pk):
		merchant_id = request.data.get("merchant_id")
		if not merchant_id:
			return Response({"merchant_id": "merchant_id is required"}, status=status.HTTP_400_BAD_REQUEST)

		application = SellerApplication.objects.select_related("user").get(pk=pk)
		application.status = SellerApplication.Status.APPROVED
		application.decline_reason = None
		application.save()

		user = application.user
		user.role = User.Role.SELLER
		user.merchant_id = merchant_id
		user.save(update_fields=["role", "merchant_id"])

		return Response(SellerApplicationSerializer(application).data)


class DeclineApplicationView(generics.GenericAPIView):
	permission_classes = [IsAdminRole]
	serializer_class = SellerApplicationSerializer

	def post(self, request, pk):
		decline_reason = request.data.get("decline_reason")
		if not decline_reason:
			return Response({"decline_reason": "decline_reason is required"}, status=status.HTTP_400_BAD_REQUEST)

		application = SellerApplication.objects.select_related("user").get(pk=pk)
		application.status = SellerApplication.Status.DECLINED
		application.decline_reason = decline_reason
		application.save()

		return Response(SellerApplicationSerializer(application).data)
