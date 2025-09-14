from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from catalog.models import Product


def home(request):
    return render(request, "home.html")


def contacts(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        return HttpResponse(f"Спасибо {name}! Данные получены!!")
    return render(request, "contacts.html")


def product_list(requests):
    products = Product.objects.all()
    context = {
        "products": products
    }

    return render(requests, "product_list.html", context=context)

def product_detail(requests, pk):
    product = get_object_or_404(Product, pk=pk)
    contex = {"product": product}
    return render(requests, "product_detail.html", context=contex)
