from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100, required=True)
    password = forms.CharField(label='Password', max_length=100, required=True)
    password2 = forms.CharField(label='Re-enter Password', max_length=100, required=True)
    email = forms.CharField(label='Email', max_length=100, required=True)
    firstName = forms.CharField(label='First name', max_length=100, required=False, initial="")
    lastName = forms.CharField(label='Last name', max_length=100, required=False, initial="")