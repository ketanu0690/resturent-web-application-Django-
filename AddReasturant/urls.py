from django.urls import path
from . import views

urlpatterns = [
path('AddReasturant',views.AddReasturant,name='AddReasturant'),
path('AddReasturantlogin',views.AddReasturantlogin),
path('AddReasturantregister',views.AddReasturantregister),
path('Addregister',views.Addregister),
path('Addlogin',views.Addlogin),
path('Insertmenu',views.Insertmenu),

]