from django.urls import path

from .views import*
urlpatterns = [

            path("", homepage, name="homepage"),
            path("login/", login_view, name="login"),
            path("logout/", logout_view, name="logout"),
            path("signup/", signup, name="signup"),
            path("products/", productlist, name="productlist"),
            path("productsdetail/<int:product_id>/", productdetails, name="productdetail"),
            path("nogotation/<int:product_id>/", negotation, name="negotation"),
            path("profile/", profile, name="profile"),
            path("report/", reportfraud, name="reportfraud"),
            path("sellproduct/", sellproduct, name="sellproduct"),
            path('edit-product/<int:product_id>/', edit_product, name='editproduct'),
            path("deleteproduct/<product_id>/", delete_product, name="deleteproduct"),
 
            ]