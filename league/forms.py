from django import forms

class NewLeagueForm(forms.Form):
    name = forms.CharField(label='League Name', max_length=100, required=True)
    description = forms.CharField(label='League Name', max_length=100, required=False)