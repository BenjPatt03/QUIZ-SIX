from rest_framework import generics, permissions, status
from rest_framework.response import Response

from services.models import Service

from .models import Order
from .serializers import OrderSerializer


class CreateOrderView(generics.CreateAPIView):
	permission_classes = [permissions.IsAuthenticated]
	serializer_class = OrderSerializer

	def create(self, request, *args, **kwargs):
		service_id = request.data.get("service")
		paypal_transaction_id = request.data.get("paypal_transaction_id")
		if not service_id:
			return Response({"service": "service is required"}, status=status.HTTP_400_BAD_REQUEST)
		if not paypal_transaction_id:
			return Response(
				{"paypal_transaction_id": "paypal_transaction_id is required"},
				status=status.HTTP_400_BAD_REQUEST,
			)

		service = Service.objects.get(pk=service_id)
		order = Order.objects.create(
			buyer=request.user,
			service=service,
			paypal_transaction_id=paypal_transaction_id,
			price_paid=service.price,
		)

		return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class UserOrderHistoryView(generics.ListAPIView):
	permission_classes = [permissions.IsAuthenticated]
	serializer_class = OrderSerializer

	def get_queryset(self):
		return Order.objects.filter(buyer=self.request.user).select_related("service").order_by("-date_purchased")
