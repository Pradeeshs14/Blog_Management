from django.db import models
from django.core.exceptions import ValidationError


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "users"

    def __str__(self):
        return self.username


class SubscriptionPlan(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    price = models.FloatField()
    max_posts = models.IntegerField(null=True)
    max_images_per_post = models.IntegerField(null=True)
    max_likes = models.IntegerField(null=True)
    max_comments = models.IntegerField(null=True)

    class Meta:
        managed = False
        db_table = "subscription_plans"

    def __str__(self):
        return self.name

    def clean(self):
        if self.price < 0:
            raise ValidationError({
                "price": "Price cannot be negative."
            })

        fields = {
            "max_posts": self.max_posts,
            "max_images_per_post": self.max_images_per_post,
            "max_likes": self.max_likes,
            "max_comments": self.max_comments,
        }

        for field, value in fields.items():
            if value is not None and value < 0:
                raise ValidationError({
                    field: f"{field.replace('_', ' ').title()} cannot be negative."
                })


class Subscription(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    plan_id = models.IntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.IntegerField()

    class Meta:
        managed = False
        db_table = "subscriptions"

    def __str__(self):
        return f"Subscription {self.id}"


class BillingHistory(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    plan_id = models.IntegerField()
    plan_name = models.CharField(max_length=50)
    price = models.FloatField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    transaction_id = models.CharField(max_length=100)
    invoice_path = models.CharField(max_length=500, null=True)

    class Meta:
        managed = False
        db_table = "billing_history"

    def __str__(self):
        return self.transaction_id