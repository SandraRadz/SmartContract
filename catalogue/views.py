from django.shortcuts import render


def home(request):
    context = {"title": "Smart Contract"}
    return render(request, "catalogue/home.html", context=context)