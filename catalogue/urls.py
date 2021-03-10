from django.urls import path

from catalogue.views import home, ProductDetailView, my_sales_view, my_shopping_view, create_new_sale

urlpatterns = [
    path("", home, name="homepage"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("product/my-sales", my_sales_view, name="my-sales"),
    path("product/my-shopping", my_shopping_view, name="my-shopping"),
    path("product/create-new-sale", create_new_sale, name="create-new-sale")
]
