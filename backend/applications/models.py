from django.conf import settings
from django.db import models


class SellerApplication(models.Model):
	class Status(models.TextChoices):
		PENDING = "Pending", "Pending"
		APPROVED = "Approved", "Approved"
		DECLINED = "Declined", "Declined"

	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="seller_application")
	status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING)
	decline_reason = models.TextField(blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.user.email} - {self.status}"
