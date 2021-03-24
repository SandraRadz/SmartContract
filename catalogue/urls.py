from django.urls import path

from catalogue.views import home, my_sales_view, my_shopping_view, create_new_sale, product_view, approve_error_view, \
    approve_receive_view, approve_send_view, solver_view

urlpatterns = [
    path("", home, name="homepage"),
    path("product/<int:product_id>/", product_view, name="product-detail"),
    path("product/my-sales", my_sales_view, name="my-sales"),
    path("product/my-shopping", my_shopping_view, name="my-shopping"),
    path("product/solver-page", solver_view, name="solver-page"),
    path("product/create-new-sale", create_new_sale, name="create-new-sale"),
    path("send_product/<int:product_id>/", approve_send_view, name="send_product"),
    path("receive_product/<int:product_id>/", approve_receive_view, name="receive_product"),
    path("problem_product/<int:product_id>/", approve_error_view, name="problem_product"),
]
