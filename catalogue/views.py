from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import DetailView

from catalogue.forms import ProductForm
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


def create_new_sale(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            description = form.cleaned_data["description"]
            price = form.cleaned_data["price"]
            product = Product(name=name, description=description, price=price, owner=request.user)
            product.save()
            return redirect(reverse("homepage"))
    else:
        form = ProductForm()
        context = {"form": form}
        return render(request, "catalogue/create_new_sale.html", context=context)
