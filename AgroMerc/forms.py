from django import forms

class datos(forms.Form):
    data=forms.CharField(widget=forms.Textarea)