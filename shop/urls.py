from django.urls import path
from . import views

urlpatterns = [
    path('item/<int:pk>/', views.item_detail, name='item_detail'),
    path('buy/<int:pk>/', views.buy_item, name='buy_item'),
    path('order/<int:pk>/', views.order_detail, name='order_detail'),
    path('buy/order/<int:pk>/', views.buy_order, name='buy_order'),
    path('success/', views.success, name='success'),
]
