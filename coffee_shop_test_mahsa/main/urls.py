from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('products/<int:category_id>/', views.products_by_category, name='products_by_category'),
    path('purchase_list/', views.purchase_list, name='purchase_list'),
    path('purchase_records/', views.purchase_records, name='purchase_records'),
]
