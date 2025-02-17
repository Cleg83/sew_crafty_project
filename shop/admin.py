from django.contrib import admin
from .models import Product, Category

# Register your models here.

class ShopAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'in_stock',
        'permanently_unavailable',
    )
    list_filter = ('category', 'in_stock', 'permanently_unavailable')
    search_fields = ('name', 'sku')
    ordering = ('sku',)

    # Disables bulk deletion on products
    actions = None  

    def has_delete_permission(self, request, obj=None):
        return False  # Completely disables product deletion


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'display_name',
        'name',
    )


admin.site.register(Product,  ShopAdmin)
admin.site.register(Category, CategoryAdmin)
