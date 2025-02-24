from django.urls import path,include
from . import views

urlpatterns = [
  
   
    path('',views.home,name='homepage'),
    path('brand/<slug:brand_slug>/',views.home,name='brand_wise_card'),
    path('details/<int:pk>', views.Details.as_view(), name='details'),
    path('profile/',views.ProfileView.as_view(),name='profile'),
    path("deposit/",views.Deposite_View.as_view(), name="deposit_money"),
    path('borrow/<slug:slug>/',views.BorrowBook.as_view(), name="borrow_book"),
     path('book/return/<slug:slug>/',views.ReturnBorrowedBook.as_view(), name="return_book"),



   
    
 
]