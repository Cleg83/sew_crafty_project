from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop_items, name='shop'),
    path('<int:shop_item_id>/', views.shop_item_info, name='shop_item_info'),
    path('manage_shop/', views.manage_shop, name='manage_shop'),
    path('add_shop_item/', views.add_shop_item, name='add_shop_item'),
    path('edit_shop_item/<int:shop_item_id>', views.edit_shop_item, name='edit_shop_item'),
    path('add_category/', views.add_category, name='add_category'),
    path('edit_category/<int:category_id>/', views.edit_category, name='edit_category'),
]