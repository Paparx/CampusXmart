from rest_framework import serializers
from .models import *

#  USER 
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = ("user_id","created_datetime", "updated_datetime")


#  CATEGORY 
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ("created_datetime", "updated_datetime")


#  PRODUCT 
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ("created_datetime", "updated_datetime")


#  TRANSACTION and sellerRating serializers removed (models not present)


#  FRAUD REPORT 
class FraudReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = FraudReport
        fields = "__all__"
        read_only_fields = ("report_issue_date",)