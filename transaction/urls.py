from django.urls import path
from . import views
urlpatterns = [
    path('deposite/', views.DepositeView, name='deposite'),
]
