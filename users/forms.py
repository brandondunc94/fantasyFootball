from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100, required="true")
    password = forms.CharField(label='Password', max_length=100, required="true")

class SignUpForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100, required ="true")
    firstName = forms.CharField(label='First Name', max_length=100, required="false")
    lastName = forms.CharField(label='Last Name', max_length=100, required="false")
    email = forms.EmailField(label='Email', max_length=100, required="true")
    password = forms.CharField(label='Password', max_length=100, required="true")