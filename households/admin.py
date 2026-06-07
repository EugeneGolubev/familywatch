from django.contrib import admin

from .models import Household, HouseholdMembership


class HouseholdMembershipInline(admin.TabularInline):
    model = HouseholdMembership
    extra = 0
    autocomplete_fields = ("user",)


@admin.register(Household)
class HouseholdAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "default_country", "created_at")
    search_fields = ("name", "owner__username", "owner__email")
    list_filter = ("default_country", "created_at")
    autocomplete_fields = ("owner",)
    inlines = (HouseholdMembershipInline,)


@admin.register(HouseholdMembership)
class HouseholdMembershipAdmin(admin.ModelAdmin):
    list_display = ("household", "user", "role", "joined_at")
    search_fields = ("household__name", "user__username", "user__email")
    list_filter = ("role", "joined_at")
    autocomplete_fields = ("household", "user")
