from django.urls import path
from . import views

handler404 = 'buyback.custom_404_view'  # Update with your view path

urlpatterns = [
    path("", views.index, name="index"),
    path('all_item_tax/', views.all_item_tax_view, name='all_item_tax'),
    path('update_inventory/', views.update_inventory, name='update_inventory'),
    path('collapsible_tree/', views.collapsible_tree_view, name='collapsible_tree'),

]
