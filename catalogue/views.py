from django.shortcuts import render
from django.views.generic import DetailView

from catalogue.models import Product


def home(request):
    context = {"title": "Smart Contract"}
    context["products"] = Product.objects.all()
    return render(request, "catalogue/home.html", context=context)


class ProductDetailView(DetailView):
    model = Product
    template_name = "catalogue/product.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def my_sales_view(request):
    context = {}
    context["products"] = Product.objects.all()
    return render(request, "catalogue/my_sales.html", context=context)


def my_shopping_view(request):
    context = {}
    context["products"] = Product.objects.all()
    return render(request, "catalogue/my_shopping.html", context=context)

