from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_basket, name='view_basket'),
    path('add/<item_id>/', views.add_to_basket, name='add_to_basket'),
    path('delete/<item_id>', views.delete_from_basket, name='delete_from_basket'),
    path('adjust/<item_id>', views.adjust_basket, name='adjust_basket'),
]