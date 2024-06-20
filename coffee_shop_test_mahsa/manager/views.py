from django.shortcuts import render, redirect
from main.models import Product
from .models import RawMaterial, ProductMaterial

def manage(request):
    return render(request, 'manager/manage.html')

def manage_storage(request):
    materials = RawMaterial.objects.all()
    if request.method == 'POST':
        for material in materials:
            material.stock = request.POST[f'stock_{material.id}']
            material.save()
        return redirect('manager:manage_storage')
    return render(request, 'manager/manage_storage.html', {'materials': materials})

def add_product(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        price = request.POST['price']
        image = request.FILES['image']
        stock = request.POST['stock']
        category_id = request.POST['category']
        category = Category.objects.get(id=category_id)
        product = Product.objects.create(name=name, description=description, price=price, image=image, stock=stock, category=category)
        # Handle raw materials for the product if needed
        return redirect('manager:manage')
    categories = Category.objects.all()
    return render(request, 'manager/add_product.html', {'categories': categories})
