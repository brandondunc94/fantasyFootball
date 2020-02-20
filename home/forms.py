from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100, required="true")
    password = forms.CharField(label='Password', max_length=100, required="true")

class SignUpForm(forms.Form):
    firstName = forms.CharField(label='First Name', max_length=100, required="true")
    lastName = forms.CharField(label='Last Name', max_length=100, required="true")
    email = forms.EmailField(label='Email', max_length=100, required="true")
    password = forms.CharField(label='Password', max_length=100, required="true")