from django.urls import path,include
from . import views

urlpatterns = [

    path('registration/',views.UserRegistrationForm.as_view(),name='registration'),
    path('login/',views.userlogin.as_view(),name='login'),
    path('logout/',views.user_logout,name='logout'),

]