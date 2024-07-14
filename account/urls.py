from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('registar/',views.UserRegistration.as_view() , name = 'register' ),
    path('logout/',LogoutView.as_view() , name = 'logout' ),
    path('login/',views.UserLoginView.as_view() , name = 'login' ),
    # path('profile/',UserProfileView.as_view() , name = 'profile' ),
    path('profile/',views.UserProfileView , name = 'profile' ),

]
