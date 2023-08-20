from django.contrib import admin
from django.urls import path, re_path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    # path('', views.LOGIN_check, name='LOGIN_check'),  # Landing page will start from here
    # path('admin/', admin.site.urls),
    # path('Home/', views.main, name='Home'),
    # path('register/', views.register, name='register'),
    # path('login/', views.login, name='login'),
    # re_path(r'^logout/(?P<username>\w+)/$', views.logout, name="logout"),
    # re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
    # re_path(r'^order(?P<orderId>\d+)/$', views.order, name='order'),
    # path('Menu/', views.MenuItems, name='Menu'),
    # path('', include('AddReasturant.urls')),
    # path('', include('chat.urls')),
    # path('updatecart/', views.updatecart, name='updatecart'),
    # re_path(r'^ViewProducts(?P<orderId>\d+)/$', views.ViewProducts, name='ViewProducts'),
    # re_path(r'^AddToCart(?P<username>[\w.@+-]+)/$', views.AddToCart, name='AddToCart'),
    # re_path(r'^CheckOut(?P<username>[\w.@+-]+)/$', views.CheckOut, name='CheckOut'),
    # path('shipping/', views.shipping, name='shipping'),
    # path('recipe/', views.recipe, name='recipe'),
    # path('searchResult/', views.searchResult, name='searchResult'),
    # path('Dashboard/', views.Dashboard, name='Dashboard'),
    path('admin/', admin.site.urls),
    path('', include('radioparts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
