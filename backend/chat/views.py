import re

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView


class AIChatbotView(APIView):
	permission_classes = [permissions.AllowAny]

	def post(self, request):
		question = (request.data.get("question") or "").strip()
		if not question:
			return Response({"question": "question is required"}, status=status.HTTP_400_BAD_REQUEST)

		q = question.lower()

		allowed_keywords = [
			"hvac",
			"heating",
			"ventilation",
			"air",
			"ac",
			"service",
			"seller",
			"admin",
			"order",
			"paypal",
			"merchant",
			"price",
			"duration",
			"rating",
			"application",
		]

		if not any(k in q for k in allowed_keywords):
			return Response(
				{
					"answer": (
						"I can only answer questions about the HVAC Service Platform "
						"(services, sellers, orders, payments, and account roles)."
					)
				}
			)

		# Simple FAQ-style responses
		if re.search(r"\bapply\b.*\bseller\b|\bseller\b.*\bapply\b", q):
			answer = "Go to the Apply Seller page, submit your application, and wait for Admin approval."
		elif "paypal" in q or "payment" in q:
			answer = (
				"Payments are handled via PayPal and are sent to the approved Seller (multi-merchant). "
				"After a successful payment, the order is recorded in your account order history."
			)
		elif "service" in q and ("add" in q or "create" in q):
			answer = "Approved Sellers can add services from the Seller Dashboard (name, description, price, duration, image)."
		elif "admin" in q and ("approve" in q or "decline" in q):
			answer = "Admins can approve/decline seller applications from the Users screen. Approve assigns a merchant-id."
		else:
			answer = "Ask about services, sellers, orders, or PayPal payments in this HVAC platform."

		return Response({"answer": answer})
