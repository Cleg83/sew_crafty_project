from django.urls import path
from . import views

urlpatterns = [
    path('', views.upcoming_events, name='events'),
    path('manage_events/', views.manage_events, name='manage_events'),
    path('add/', views.add_event, name='add_event'),
    path('edit/<int:event_id>/', views.edit_event, name='edit_event'),
    path('delete/<int:event_id>/', views.delete_event, name='delete_event'),
]