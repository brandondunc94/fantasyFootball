from django import forms

INTEGER_CHOICES= [tuple([x,x]) for x in range(1,32)]

class LeagueForm(forms.Form):
    leagueName= forms.CharField(max_length=100)
    = forms.CharField(max_length=100)
    email= forms.EmailField()
    age= forms.IntegerField()
    todays_date= forms.IntegerField(label="What is today's date?", widget=forms.Select(choices=INTEGER_CHOICES))
