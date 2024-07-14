from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
from .forms import DepositeForm
from django.contrib import messages
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string


def send_transaction_email(user, amount, subject, template):
        message = render_to_string(template, {
            'user' : user,
            'amount' : amount,
        })
        send_email = EmailMultiAlternatives(subject, '', to=[user.email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()



@login_required
def DepositeView(request):
    if request.method == 'POST':
        form = DepositeForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            request.user.account.balance += amount
            request.user.account.save()
            messages.success(request, f'Deposited {amount}$ successfully.')
            send_transaction_email(request.user, amount, "Deposite Message", "deposite_email.html")
            return redirect('home')
    else:
        form = DepositeForm()
    return render(request, 'deposits.html', {'form': form})