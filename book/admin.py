from django.contrib import admin
from .models import BookModel,BorrowBook,Comment
# Register your models here.
admin.site.register(BookModel)
admin.site.register(BorrowBook)
admin.site.register(Comment)