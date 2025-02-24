from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from . models import UserAccount

class RegistrationForm(UserCreationForm):
    address = forms.CharField(max_length=2049)
    first_name = forms.CharField(
        max_length=255, widget=forms.TextInput(attrs={'id': 'required'}))
    last_name = forms.CharField(
        max_length=255, widget=forms.TextInput(attrs={'id': 'required'}))
    email = forms.EmailField(
        max_length=255, widget=forms.EmailInput(attrs={'id': 'required'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'password1', 'password2', 'email', 'address']

    def save(self, commit=True):
        our_user = super().save(commit=False)
        if commit:
            our_user.save()
            address = self.cleaned_data.get('address')
            UserAccount.objects.create(user=our_user, address=address)
        return our_user

