from django.contrib import admin
from apps.payment import models


@admin.register(models.Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


@admin.register(models.Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ["user", "plan", "status", "start_date", "end_date", "updated_at", "created_at"]
    list_filter = ["plan", "status", "start_date", "end_date"]
    search_fields = ["user"]
