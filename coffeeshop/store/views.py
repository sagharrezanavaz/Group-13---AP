import django
from django.contrib.auth.models import User
from .models import  Cart, Category, Order, Product, Storage
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect, render, get_object_or_404
from .forms import RegistrationForm
from django.contrib import messages
from django.views import View
import decimal
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator # for Class Based Views
from store.models import  Cart, Category, Order, Product
from django.shortcuts import render, redirect
from .forms import ProductForm
import pandas as pd
from django_pandas.io import read_frame
import plotly
import plotly.express as px
import json
from django.db.models import Sum


def home(request):
    categories = Category.objects.filter()[:3]
    products = Product.objects.annotate(total_quantity_sold=Sum('order__quantity')).order_by('-total_quantity_sold')[:12]
    context = {
        'categories': categories,
        'products': products,
    }
    return render(request, 'store/index.html', context)

@user_passes_test(lambda u: u.is_staff)
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('store:home')  # Redirect to a page displaying the list of products
    else:
        form = ProductForm()
    
    return render(request, 'add-product.html', {'form': form})

def detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.exclude(id=product.id).filter(category=product.category)
    context = {
        'product': product,
        'related_products': related_products,

    }
    return render(request, 'store/detail.html', context)


def all_categories(request):
    categories = Category.objects.filter()
    return render(request, 'categories.html', {'categories':categories})


def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    categories = Category.objects.filter()
    context = {
        'category': category,
        'products': products,
        'categories': categories,
    }
    return render(request, 'categories.html', context)



class RegistrationView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'account/register.html', {'form': form})
    
    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, "Congratulations! Registration Successful!")
            form.save()
        return render(request, 'account/register.html', {'form': form})
        

@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'account/profile.html', { 'orders':orders})


@method_decorator(login_required, name='dispatch')
class AddressView(View):
    def get(self, request):
        return render(request, {'form': form})




@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = get_object_or_404(Product, id=product_id)
    
    # Check if there are enough ingredients in the storage for this product
    if check_ingredients_availability(product):
        add_product_to_cart_and_deduct_ingredients(product, user)
        messages.success(request, 'Your orders have been added successfully.')
        return redirect('store:cart')
    else:
        messages.error(request, "Unable to add product to cart. Required ingredients not available.")
        return redirect('store:home')  # Redirect to homepage or a specific page indicating ingredient unavailability

def add_product_to_cart_and_deduct_ingredients(product, user):
    item_already_in_cart = Cart.objects.filter(product=product, user=user).first()
    if item_already_in_cart:
        item_already_in_cart.quantity += 1
        item_already_in_cart.save()
    else:
        Cart(user=user, product=product).save()
    
    deduct_ingredient_amounts(product)

def deduct_ingredient_amounts(product):
    ingredients = {
        'Sugar': product.Sugar,
        'Coffee': product.Coffee,
        'Flour': product.Flour,
        'Chocolate': product.Chocolate,
        'Milk': product.Milk
    }
    
    for ingredient, quantity_needed in ingredients.items():
        storage_item = Storage.objects.filter(name=ingredient).first()
        if storage_item:
            storage_item.amount -= quantity_needed
            storage_item.save()
def check_ingredients_availability(product):
    # Define a method to check if there are enough ingredients in the storage for a given product
    ingredients = {
        'Sugar': product.Sugar,
        'Coffee': product.Coffee,
        'Flour': product.Flour,
        'Chocolate': product.Chocolate,
        'Milk': product.Milk
    }
    
    for ingredient, quantity_needed in ingredients.items():
        storage_item = Storage.objects.filter(name=ingredient).first()
        if not storage_item or storage_item.amount < quantity_needed:
            return False

    return True

@login_required
def cart(request):
    user = request.user
    cart_products = Cart.objects.filter(user=user)

    amount = decimal.Decimal(0)
    shipping_amount = decimal.Decimal(10)
    cp = [p for p in Cart.objects.all() if p.user==user]
    if cp:
        for p in cp:
            temp_amount = (p.quantity * p.product.price)
            amount += temp_amount


    context = {
        'cart_products': cart_products,
        'amount': amount,
        'shipping_amount': shipping_amount,
        'total_amount': amount + shipping_amount,
    }

    return render(request, 'cart.html', context)


@login_required
def remove_cart(request, cart_id):
    if request.method == 'GET':
        c = get_object_or_404(Cart, id=cart_id)
        c.delete()
        messages.success(request, "Product removed from Cart.")
    return redirect('store:cart')


@login_required
def plus_cart(request, cart_id):
    if request.method == 'GET':
        cp = get_object_or_404(Cart, id=cart_id)
        cp.quantity += 1
        cp.save()
    return redirect('store:cart')

@login_required
def minus_cart(request, cart_id):
    if request.method == 'GET':
        cp = get_object_or_404(Cart, id=cart_id)
        if cp.quantity == 1:
            cp.delete()
        else:
            cp.quantity -= 1
            cp.save()
    return redirect('store:cart')


@login_required
def checkout(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    for c in cart:
        Order(user=user, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect('store:orders')


@login_required
def orders(request):
    all_orders = Order.objects.filter(user=request.user).order_by('-ordered_date')
    messages.success(request, 'Your orders have been loaded successfully.')  # Add success message
    return render(request, 'cart.html', {'orders': all_orders})



def shop(request):
    return render(request, 'store/shop.html')





def test(request):
    return render(request, 'store/test.html')

@user_passes_test(lambda u: u.is_staff)
def storage(request):
    storage_items = Storage.objects.all()

    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        new_amount = request.POST.get('new_amount')
        storage_item = Storage.objects.get(id=item_id)
        storage_item.amount = new_amount
        storage_item.save()

    return render(request, 'storage.html', {'storage_items': storage_items})


@user_passes_test(lambda u: u.is_staff)
def store_management(request):
    products = Product.objects.all()

    product_id = request.GET.get('product_id')
    sales_data = []
    selected_product = None

    if product_id:
        selected_product = Product.objects.get(id=product_id)
        orders = Order.objects.filter(product__id=product_id).order_by('ordered_date')
       
        df = read_frame(orders)
        df['ordered_date'] = pd.to_datetime(df['ordered_date'])  # Convert 'ordered_date' to datetime if it's not already
       
        grouped_orders = df.groupby('ordered_date')['quantity'].sum().reset_index()  # Group by 'ordered_date' and sum 'quantity'

        sales_graph = px.bar(grouped_orders, x='ordered_date', y='quantity', title="Sales Graph")
        sales_graph = json.dumps(sales_graph, cls=plotly.utils.PlotlyJSONEncoder)

        sales_data.append({'sales_graph': sales_graph})

    return render(request, 'store-management.html', {'products': products, 'selected_product': selected_product, 'sales_data': sales_data})
