from django import forms

class LeagueForm(forms.Form):
    leagueName= forms.CharField(max_length=100)

class LeagueList(forms.Form):
    

