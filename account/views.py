from django.shortcuts import render
from django.views.generic import FormView
from .forms import UserRegistrationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.views import View
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from book.models import BorrowBook
from django.contrib.auth.decorators import login_required

class UserRegistration(FormView):
    template_name = 'register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('profile')
    
    def form_valid(self, form):
        print(form.cleaned_data)
        user = form.save()
        login(self.request, user)
        # messages.success(self.request , "Account created successfully")
        print(user)
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Register'
        return context
    

class UserLoginView(LoginView):
    template_name = 'register.html'
    def get_success_url(self):
        return reverse_lazy('profile')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Login'
        return context

    
# class UserProfileView(LoginRequiredMixin,View):
#     template_name = 'profile.html'
@login_required
def UserProfileView(request):
    borrow_books = BorrowBook.objects.filter(user=request.user)
    return render(request , 'profile.html' , {'borrow_books':borrow_books})

