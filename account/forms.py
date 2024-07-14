from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import UserLibraryAccount

class UserRegistrationForm(UserCreationForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'birth_date','password1', 'password2',]

    def save(self,commit=True):
        our_user = super().save(commit=False)
        if commit == True:
            our_user.save()
            birth_date = self.cleaned_data.get('birth_date')

            UserLibraryAccount.objects.create(
                user = our_user,
                birth_date =birth_date,
                account_no = 100+ our_user.id
            )
        return our_user