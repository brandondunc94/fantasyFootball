from django import forms

CHOICES=[('Public',''),('Private', '')]

class NewLeagueForm(forms.Form):
    name = forms.CharField(label='League Name', max_length=100, required=True)
    description = forms.CharField(label='League Name', max_length=100, required=False)
    visibility = forms.ChoiceField(label='League Visibility', choices=CHOICES, widget=forms.RadioSelect)
