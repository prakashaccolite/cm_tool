from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.register,name='register'),
    path('login/',views.login_page,name='login'),
    path('logout/',views.logout_user,name="logout"),
    path('', views.home,name='home'),
    path('products/',views.products,name='products'),
    path('customer/<str:key>/',views.customer,name='customer'),
    path('create_order/',views.createOrder,name='create_order'),
    path('update_order/<str:key>/',views.updateOrder,name='update_order'),

]