from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "display_name", "preferred_country")
    search_fields = ("user__username", "user__email", "display_name")
    list_filter = ("preferred_country",)
