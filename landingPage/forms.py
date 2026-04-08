from django import forms

class SubscribeForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'required email',
            'id': 'mce-EMAIL',
            'placeholder': 'e-mail',
        })
    )
    honeypot = forms.CharField(
        required=False, 
        widget=forms.HiddenInput(attrs={
            'tabindex': '-1',
            'value': ''
        })
    )