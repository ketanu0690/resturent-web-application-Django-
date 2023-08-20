from django.urls import path
from . import views

app_name = 'radioparts'

urlpatterns = [
    path('', views.PartsListView.as_view(), name='parts_list'),
    # path('parts/<int:pk>/add-to-cart/', views.AddToCartView.as_view(), name='add-to-cart'),
    # path('cart/<int:pk>/remove/', views.RemoveFromCartView.as_view(), name='remove-from-cart'),
    # path('login/', views.LoginView.as_view(), name='login'),
    # path('register/', views.RegisterView.as_view(), name='register'),
    # path('admin/parts/<int:pk>/update/', views.AdminPartUpdateView.as_view(), name='admin-part-update'),
]
