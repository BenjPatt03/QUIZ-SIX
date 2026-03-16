from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):
	def create_user(self, username, email=None, password=None, **extra_fields):
		if not email:
			raise ValueError("Email is required")
		email = self.normalize_email(email)
		user = self.model(username=username, email=email, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, username, email=None, password=None, **extra_fields):
		extra_fields.setdefault("is_staff", True)
		extra_fields.setdefault("is_superuser", True)
		extra_fields.setdefault("role", CustomUser.Role.ADMIN)
		return self.create_user(username=username, email=email, password=password, **extra_fields)


class CustomUser(AbstractUser):
	class Role(models.TextChoices):
		ADMIN = "Admin", "Admin"
		SELLER = "Seller", "Seller"
		USER = "User", "User"

	email = models.EmailField(unique=True)
	phone_number = models.CharField(max_length=32, blank=True)
	location = models.CharField(max_length=255, blank=True)
	gender = models.CharField(max_length=32, blank=True)
	role = models.CharField(max_length=16, choices=Role.choices, default=Role.USER)
	merchant_id = models.CharField(max_length=128, blank=True, null=True)

	objects = CustomUserManager()

	USERNAME_FIELD = "email"
	REQUIRED_FIELDS = ["username"]

	def __str__(self):
		return f"{self.email} ({self.role})"

# Create your models here.
