
from django.urls import path
from . import views
urlpatterns = [
    path('register/',views.registerview),
    path('login/',views.loginview),
    path('user/',views.userview),
    path('logout/',views.logoutview),
]
