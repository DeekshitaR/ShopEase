# Shop/admin.py
from django.contrib import admin
from .models import Product, CartItem, Order

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','name','price')
    search_fields = ('name',)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id','user','product','quantity')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','user','total_amount','created_at')
    readonly_fields = ('created_at',)
