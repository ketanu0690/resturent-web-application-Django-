
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from .import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Home',views.main,name='Home'),
    path('register',views.register),
    path('login',views.login),
    url(r'^logout/(?P<username>\w+)/$',views.logout,name="logout"),
    path('activate/<uidb64>/<token>',views.activate,name='activate'),
    path('',views.LOGIN_check,name='LOGIN_check'),
    path('order<orderId>',views.order,name='order'),
    path('Menu',views.MenuItems,name='Menu'),
    path('',include('AddReasturant.urls')),
    # path('',include('chat.urls')),
    path('updatecart',views.updatecart,name='updatecart'),
    path('ViewProducts<orderId>',views.ViewProducts,name='ViewProducts'),
    path('AddToCart',views.AddToCart,name='AddToCart'),
    # path('RemoveFromCart<orderId>',views.RemoveFromCart,name='RemoveFromCart'),
    path('CheckOut',views.CheckOut,name='CheckOut'),

]
