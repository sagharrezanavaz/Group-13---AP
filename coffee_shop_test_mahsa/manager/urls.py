from django.urls import path
from . import views

app_name = 'manager'

urlpatterns = [
    path('', views.manage, name='manage'),
    path('storage/', views.manage_storage, name='manage_storage'),
    path('add_product/', views.add_product, name='add_product'),
]
