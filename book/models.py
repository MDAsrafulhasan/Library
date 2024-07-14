from django.db import models
from category.models import CategoryBooks
from django.contrib.auth.models import User
# Create your models here.
class BookModel(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='./book./media./uploads./')
    borrowing_price = models.DecimalField(max_digits=10, decimal_places=2)
    categories = models.ManyToManyField(CategoryBooks)
    def __str__(self):
        return self.title

class BorrowBook(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='borrowed_books')
    book = models.ForeignKey(BookModel, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    is_returned =models.BooleanField(default=False , blank=True , null=True)

    def __str__(self):
        return f'{self.user.username} borrowed {self.book.title}'
    
class Comment(models.Model):
    book = models.ForeignKey(BookModel, on_delete=models.CASCADE,related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'Comment by {self.user.username}'