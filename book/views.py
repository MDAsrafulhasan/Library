from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from .models import BookModel,BorrowBook
from . import models
from . import forms
from django.contrib import messages
from transaction.views import send_transaction_email
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

# class DetailPostView(DetailView):
#     model = models.BookModel
#     pk_url_kwarg = 'id'
#     template_name = 'book_details.html'

def DetailPostView(request, id):
    book = BookModel.objects.get(pk=id)
    comments = models.Comment.objects.filter(book=book)
    # borrow_book = BorrowBook.objects.filter(user=request.user, book=book).exists()
    borrow_book = False
    if request.user.is_authenticated:
        borrow_book = BorrowBook.objects.filter(user=request.user, book=book).exists()

    if request.method == 'POST' and borrow_book:
        form = forms.CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.book = book
            comment.save()
            return redirect('detail_book', id)
    else:
        form = forms.CommentForm()

    # context = {'book': book,'borrowed': borrow_book,'comment_form': form,'comments': comments,}
    return render(request, 'book_details.html', {'book': book,'borrowed': borrow_book,'comment_form': form, 'comments': comments})

    

@login_required
def Borrow_Book(request , id):
    book = models.BookModel.objects.get(pk = id)
    user_ac = request.user.account

    borrow_book = models.BorrowBook.objects.filter(user=request.user, book=book, is_returned=False)

    if borrow_book:
        messages.error(request, 'You have already borrowed this book. Please return it first.')
        return redirect('detail_book', id)

    if user_ac.balance<book.borrowing_price:
        messages.error(request, 'You do not have enough balance to borrow this book.')
        return redirect('detail_book', id)
    
    if request.method == 'POST':
        BorrowBook.objects.create(user = request.user , book = book)
        user_ac.balance -= book.borrowing_price
        user_ac.save()

        messages.success(request, 'Book borrowed successfully.')
        # send_transaction_email(request.user, book.borrowing_price, "Borrow Book Message", "borrow_book_email.html")

        mail_subject = "Borrow Book Message"
        message = render_to_string('borrow_book_email.html', {'user': request.user , 'name':book.title , 'amount':book.borrowing_price})
        to_email = request.user.email
        send_email = EmailMultiAlternatives(mail_subject, '', to=[to_email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()
        return redirect('detail_book', id)
    
    
# def ReturnBook(request,id):
#     borrow_book = models.BorrowBook.objects.get(pk = id)
#     user_ac = request.user.account

#     user_ac.balance += borrow_book.book.borrowing_price
#     user_ac.save()
#     borrow_book.is_returned = True
#     borrow_book.save()
    
#     # borrow_book = get_object_or_404(models.BorrowBook, user=request.user, book=book)
#     # borrow_book.is_returned = True
#     # borrow_book.save()
#     messages.success(request,'Book returned successfully')
#     return redirect('profile')

@login_required
def ReturnBook(request,id):
    book = models.BookModel.objects.get(pk = id)
    user_ac = request.user.account

    user_ac.balance += book.borrowing_price
    user_ac.save()
    borrow_book = get_object_or_404(models.BorrowBook, user=request.user, book=book ,is_returned = False)
    borrow_book.is_returned = True
    borrow_book.save()

    messages.success(request,'Book returned successfully')
    return redirect('profile')