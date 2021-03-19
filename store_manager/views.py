from django.shortcuts import render

from products.models import Category, Product

def homePage(request):
    cat = Category.objects.get(pk=81)
    for i in range(1000):
        Product.objects.create(name=f"product {i}", category=cat, price=i, box_quantity=i * 2)
    return render(request, 'home.html', {})