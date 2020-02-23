from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', max_length=100)
    #email = forms.CharField(label='Email', max_length=100)
    #firstName = forms.CharField(label='First name', max_length=100)
    #lastName = forms.CharField(label='Last name', max_length=100)