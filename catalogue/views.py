from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import DetailView

from accounts.models import User
from catalogue.forms import ProductForm, SolversForm
from catalogue.models import Product, PurchaseStatus


def home(request):
    context = {"title": "Smart Contract"}
    context["products"] = Product.objects.filter(status=PurchaseStatus.NEW).order_by('-created_at')
    return render(request, "catalogue/home.html", context=context)


class ProductDetailView(DetailView):
    model = Product
    template_name = "catalogue/product.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def product_view(request, product_id):
    product = Product.objects.get(pk=product_id)
    if request.method == "POST":
        form = SolversForm(product, request.POST)
        if form.is_valid():
            solver = form.cleaned_data["solver"]
            print(solver)
            solver_obj = User.objects.filter(pk=solver).first()
            product.final_solver = solver_obj
            product.buyer = request.user
            product.save()
            return redirect(reverse("my-shopping"))
    else:
        form = SolversForm(product)
    context = {"form": form, "object": product}
    return render(request, "catalogue/product.html", context=context)


def my_sales_view(request):
    context = {}
    context["products"] = Product.objects.filter(owner=request.user).order_by('-updated_at')
    return render(request, "catalogue/my_sales.html", context=context)


def my_shopping_view(request):
    context = {}
    context["products"] = Product.objects.filter(buyer=request.user).order_by('-updated_at')
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
            solvers = form.cleaned_data["solvers"]
            for solver in solvers:
                product.solver_list.add(solver)
            return redirect(reverse("homepage"))
    else:
        form = ProductForm()
        context = {"form": form}
        return render(request, "catalogue/create_new_sale.html", context=context)


def buy_product_view(request):
    pass
