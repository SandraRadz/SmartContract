from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import DetailView

from accounts.models import User
from catalogue.forms import ProductForm, SolversForm
from catalogue.models import Product, PurchaseStatus
from .tasks import submit_new_smart_contract, send_product, receive_product


def home(request):
    context = {"title": "Smart Contract"}
    context["products"] = Product.objects.filter(status=PurchaseStatus.NEW).order_by('-created_at')
    return render(request, "catalogue/home.html", context=context)


def product_view(request, product_id):
    product = Product.objects.get(pk=product_id)
    if request.method == "POST":
        form = SolversForm(product, request.POST)
        if form.is_valid():
            solver = form.cleaned_data["solver"]
            solver_obj = User.objects.filter(pk=solver).first()
            product.final_solver = solver_obj
            buyer = request.user
            product.buyer = buyer
            product.status = PurchaseStatus.PENDING_ORDER
            product.save()
            submit_new_smart_contract.delay(product.owner.escrow_hash, solver_obj.escrow_hash, buyer.private_hash,
                                            product.price, product.id)
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


def solver_view(request):
    context = {}
    context["products"] = Product.objects.filter(final_solver=request.user, status=PurchaseStatus.PROBLEM).order_by('-updated_at')
    return render(request, "catalogue/solver_page.html", context=context)


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


def approve_send_view(request, product_id):
    product = Product.objects.get(pk=product_id)
    product.status = PurchaseStatus.PENDING_SEND
    product.save()
    send_product.delay(product.owner.private_hash, product.contract_address, product.id)
    return redirect(reverse("my-sales"))


def approve_receive_view(request, product_id):
    product = Product.objects.get(pk=product_id)
    product.status = PurchaseStatus.PENDING_RECEIVED
    product.save()
    receive_product.delay(product.buyer.private_hash, product.contract_address, product.id)
    return redirect(reverse("my-shopping"))


def approve_error_view(request, product_id):
    product = Product.objects.get(pk=product_id)
    product.status = PurchaseStatus.PROBLEM
    product.save()
    messages.error(request, 'Your solver will contact you in the nearest time')
    return redirect(reverse("my-shopping"))


def refund_view(request, product_id):
    product = Product.objects.get(pk=product_id)
    product.status = PurchaseStatus.PENDING_REFUND
    product.save()
    receive_product.delay(request.user.private_hash, product.contract_address, product.id)
    return redirect(reverse("solver-page"))


def no_refund_view(request, product_id):
    product = Product.objects.get(pk=product_id)
    product.status = PurchaseStatus.PENDING_NO_REFUND
    product.save()
    receive_product.delay(request.user.private_hash, product.contract_address, product.id)
    return redirect(reverse("solver-page"))