from django.urls import path

from catalogue.views import home, ProductDetailView, my_sales_view, my_shopping_view, create_new_sale, buy_product_view, \
    product_view

urlpatterns = [
    path("", home, name="homepage"),
    path("product/<int:product_id>/", product_view, name="product-detail"),
    path("product/my-sales", my_sales_view, name="my-sales"),
    path("product/my-shopping", my_shopping_view, name="my-shopping"),
    path("product/create-new-sale", create_new_sale, name="create-new-sale"),
    path("buy_product/<int:pk>/", buy_product_view, name="buy_product"),
]
