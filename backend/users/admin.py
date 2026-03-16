from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
	list_display = ("id", "email", "username", "role", "merchant_id", "is_staff")
	search_fields = ("email", "username", "first_name", "last_name")
