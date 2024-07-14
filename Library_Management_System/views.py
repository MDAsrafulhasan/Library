from django.shortcuts import render
from category.models import CategoryBooks
from django.contrib.auth.decorators import login_required
from book.models import BookModel
def homepage(request,category_slug = None):
    data = BookModel.objects.all()
    if category_slug is not None:
        category = CategoryBooks.objects.get(slug = category_slug)
        data = BookModel.objects.filter(categories  = category)
    categories = CategoryBooks.objects.all()

    return render(request, 'home.html' , {'data':data , 'categories': categories})