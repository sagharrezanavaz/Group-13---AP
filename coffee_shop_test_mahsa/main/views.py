from django.shortcuts import render, get_object_or_404
from .models import Product, Category, Purchase

def index(request):
    categories = Category.objects.all()
    most_purchased = Product.objects.order_by('-purchase__quantity')[:12]
    return render(request, 'main/index.html', {'categories': categories, 'most_purchased': most_purchased})

def products_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'main/products.html', {'category': category, 'products': products})

def purchase_list(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    purchases = Purchase.objects.filter(user=request.user)
    return render(request, 'main/purchase_list.html', {'purchases': purchases})

def purchase_records(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    purchase_records = Purchase.objects.filter(user=request.user)
    return render(request, 'main/purchase_records.html', {'purchase_records': purchase_records})
