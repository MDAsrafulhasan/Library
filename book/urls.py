

from django.urls import path
from . import views
urlpatterns = [
    # path('details/<int:id>/', views.DetailPostView.as_view(), name='detail_book'),
    path('details/<int:id>/', views.DetailPostView, name='detail_book'),
    path('borrow/<int:id>/', views.Borrow_Book, name='borrow_book'),
    path('return/<int:id>/', views.ReturnBook, name='return_book'),
]
