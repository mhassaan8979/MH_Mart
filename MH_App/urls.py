from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product, name='products'),
    path('search/', views.search, name='search'),
    path('contact/', views.contact, name='contact'),
    path('product/<str:id>', views.product_details, name='product_details'),
    path('register/', views.to_register, name='register'),
    path('login/', views.for_login, name='login'),
    path('logout/', views.for_logout, name='logout'),

    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/', views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/', views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart_detail/',views.cart_detail,name='cart_detail'),
    path('cart/check_out/',views.check_out,name='check_out'),
    path('cart/check_out/place_order/',views.place_order,name='place_order'),
    path('success/',views.success,name='success'),
]
