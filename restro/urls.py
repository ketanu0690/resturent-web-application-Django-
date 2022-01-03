
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from .import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Home',views.main),
    path('register',views.register),
    path('login',views.login),
    url(r'^logout/(?P<username>\w+)/$',views.logout,name="logout"),
    path('activate/<uidb64>/<token>',views.activate,name='activate'),
    path('',views.LOGIN_check,name='LOGIN_check'),
    path('order',views.order,name='order'),
    path('Menu',views.MenuItems,name='Menu'),
    # path('AddReasturant',include('AddReasturant'))
    path('',include('AddReasturant.urls')),

]
