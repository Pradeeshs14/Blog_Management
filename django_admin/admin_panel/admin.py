from django.contrib import admin
from .models import (
    User,
    SubscriptionPlan,
    Subscription,
    BillingHistory,
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email")
    search_fields = ("username", "email")


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "price",
        "max_posts",
        "max_images_per_post",
        "max_likes",
        "max_comments",
    )
    search_fields = ("name",)
    list_filter = ("name",)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user_id",
        "plan_id",
        "start_date",
        "end_date",
        "is_active",
    )
    search_fields = ("user_id", "plan_id")
    list_filter = ("is_active",)


@admin.register(BillingHistory)
class BillingHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user_id",
        "plan_name",
        "price",
        "transaction_id",
        "start_date",
        "end_date",
        "invoice_path",
    )
    search_fields = (
        "transaction_id",
        "plan_name",
        "user_id",
    )
    list_filter = ("plan_name",)