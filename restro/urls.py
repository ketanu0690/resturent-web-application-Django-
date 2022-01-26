
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
    path('',views.LOGIN_check,name='LOGIN_check'),# landing page will start from here
    path('order<orderId>',views.order,name='order'),
    path('Menu',views.MenuItems,name='Menu'),
    path('',include('AddReasturant.urls')),
    path('',include('chat.urls')),
    path('updatecart',views.updatecart,name='updatecart'),
    path('ViewProducts<orderId>',views.ViewProducts,name='ViewProducts'),
    path('AddToCart<username>',views.AddToCart,name='AddToCart'),
    path('CheckOut<username>',views.CheckOut,name='CheckOut'),
    path('shipping',views.shipping,name='shipping'),
    path('recipe',views.recipe,name='recipe'),
    path('searchResult',views.searchResult,name='searchResult'),
    path('Dashboard',views.Dashboard)

]
