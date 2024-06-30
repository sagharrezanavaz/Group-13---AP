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
from .models import  Cart, Category, Order, Product
from django.shortcuts import render, redirect
from .forms import ProductForm
from django.db.models import Sum
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.urls import reverse
from .utils import get_plot



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
    return render(request, 'detail.html', context)


def all_categories(request):
    categories = Category.objects.filter()
    return render(request, 'categories.html', {'categories':categories})


def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    categories = Category.objects.all()
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
        if 'item_id' in request.POST and 'new_amount' in request.POST:
            item_id = request.POST.get('item_id')
            new_amount = request.POST.get('new_amount')

            storage_item = Storage.objects.get(id=item_id)
            storage_item.amount = new_amount
            storage_item.save()
        else:
            name = request.POST.get('name')
            amount = request.POST.get('amount')

            new_item = Storage(name=name, amount=amount)
            new_item.save()

    return render(request, 'storage.html', {'storage_items': storage_items})


@user_passes_test(lambda u: u.is_staff)
def store_management(request):
    products = Product.objects.all()

    product_id = request.GET.get('product_id')

@user_passes_test(lambda u: u.is_staff)
def store_management(request):
        products = Product.objects.all()
        product_id = request.GET.get('product_id')
        sales_data = []
        selected_product = products.first()
        chart=''
        if product_id:
            selected_product = Product.objects.get(id=product_id)
            orders = Order.objects.filter(product__id=product_id).order_by('ordered_date')
            chart=''
            # Ensure we're working with the correct product
            if orders.exists():
                # Extract unique ordered dates
                ordered_dates = [order.ordered_date.date() for order in orders]

                # Initialize a dictionary to hold aggregated quantities
                aggregated_quantities = {}

                # Iterate through each unique ordered date
                for date in ordered_dates:
                    # Format the date as a string for easier comparison
                    date_str = date.strftime('%Y-%m-%d')
                    # Aggregate the quantities for this date
                    quantities = orders.filter(ordered_date__date=date).aggregate(total_quantity=Sum('quantity'))
                    # Safely access the aggregated quantity, providing a default of 0 if none exists
                    aggregated_quantities[date_str] = quantities.get('total_quantity', 0)

                # Prepare the final data structure for the template
                for date, quantity in aggregated_quantities.items():
                    sales_data.append({
                        'date': date,
                        'total_quantity_ordered': quantity
                    })
                x = [item['date'] for item in sales_data]
                y = [item['total_quantity_ordered'] for item in sales_data]
                chart=get_plot(x,y)

            else:
                # Handle the case where no orders exist for the selected product
                print("No orders found for the selected product.")

        return render(request, 'store-management.html', {'products': products, 'selected_product': selected_product, 'chart': chart})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_staff:  # Assuming admin users are identified by is_staff flag
                return redirect('store:store-management')
            else:
                return redirect('store:profile')
        else:
            login_failed = True
            return render(request, 'account/login.html', {'login_failed': login_failed})

    return render(request, 'account/login.html')