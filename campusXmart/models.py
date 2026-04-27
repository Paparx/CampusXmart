from django.db import models
import uuid
from datetime import datetime

# def profile_photo(instance, filename):
#     ext = filename.split('.')[-1]

#     user_id = instance.user_id or "newuser"
#     username = instance.user_name.replace(" ", "_").lower()

#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     unique_id = uuid.uuid4().hex[:8]

#     return f"profile_photo/user_{user_id}_{username}/{timestamp}_{unique_id}.{ext}"

# def product_photo(instance, filename):
#     ext = filename.split('.')[-1]

#     user_id = instance.user.user_id if instance.user else "nouser"
#     product_id = instance.product_id

#     title = instance.product_title[:20].replace(" ", "_").lower()

#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     unique_id = uuid.uuid4().hex[:8]

#     return f"product_photo/user_{user_id}/product_{product_id}_{title}/{timestamp}_{unique_id}.{ext}"

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


# TRANSACTIONS
class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="transactions"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="transactions"
    )
    final_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_mode = models.CharField(max_length=50)
    transaction_date = models.DateTimeField(auto_now_add=True)
    transaction_status = models.CharField(max_length=30)

    def __str__(self):
        return f"Transaction #{self.transaction_id}"


# SELLER RATINGS
class sellerRating(models.Model):
    rating_id = models.AutoField(primary_key=True)
    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="ratings_received"
    )
    
    reporter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="ratings_given"
    )
    
    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE,
        related_name="seller_ratings"
    )
    review = models.TextField()
    rating_date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Seller Rating #{self.rating_id}"


# FRAUD REPORTS
class FraudReport(models.Model):
    fraud_report_id = models.AutoField(primary_key=True)
    reported = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reports_filed"
    )
    reportee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reports_received"
    )
    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE,
        related_name="fraud_reports"
    )
    reason = models.CharField(max_length=255)
    type_of_fraud = models.CharField(max_length=100)
    any_evidence = models.CharField(max_length=255)
    description = models.TextField()
    report_issue_date = models.DateTimeField(auto_now_add=True)
    report_status = models.CharField(max_length=50)
    verification_status = models.CharField(max_length=50)

    def __str__(self):
        return f"FraudReport #{self.fraud_report_id}"

