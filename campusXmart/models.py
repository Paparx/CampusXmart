from django.db import models
import uuid
from datetime import datetime

# USERS
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=50, unique=True)
    email_id = models.EmailField(max_length=100, unique=True)
    contact_no = models.CharField(max_length=15)
    user_image_url = models.ImageField(upload_to="profile_photo")
    password = models.CharField(max_length=255)
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.user_name


# CATEGORIES
class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100, unique=True)
    category_description = models.TextField(blank=True, null=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category_name


# PRODUCTS
class Product(models.Model):
    product_id = models.AutoField(primary_key=True)

    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name="products")
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="products")
    
    product_title = models.CharField(max_length=150)
    product_description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product_image_url = models.ImageField(upload_to="product_photo")
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_title


# TRANSACTIONS and sellerRating removed — not needed in current project
# If needed in future, reintroduce Transaction and sellerRating models and run migrations.


# FRAUD REPORTS
class FraudReport(models.Model):
    fraud_report_id = models.AutoField(primary_key=True)
    # optional reporter (allow anonymous reports)
    reported = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="reports_filed",
        null=True,
        blank=True,
    )
    # optional reportee (the user being reported)
    reportee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="reports_received",
        null=True,
        blank=True,
    )
    # transaction field removed (not used in this project)
    # short subject/reason
    reason = models.CharField(max_length=255, blank=True, null=True)
    # category/type
    type_of_fraud = models.CharField(max_length=100, blank=True, null=True)
    # store uploaded evidence file
    any_evidence = models.FileField(upload_to='report_evidence', null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    report_issue_date = models.DateTimeField(auto_now_add=True)
    report_status = models.CharField(max_length=50, default='submitted')
    verification_status = models.CharField(max_length=50, default='pending')

    def __str__(self):
        return f"FraudReport #{self.fraud_report_id}"

