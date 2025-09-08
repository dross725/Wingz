from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("login", views.login, name="login-page" ),
    path("ridelist", views.Ride_Listview.as_view(), name='ridelist-page'),
    
]
