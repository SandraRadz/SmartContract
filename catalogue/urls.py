from django.urls import path

from catalogue.views import home, ProductDetailView

urlpatterns = [
    path("", home, name="homepage"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product-detail")
]
