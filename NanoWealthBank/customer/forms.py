from django import forms

class EmailForm(forms.Form):
    email = forms.EmailField(label='Enter your email')

class VerificationForm(forms.Form):
    code = forms.CharField(label='Enter verification code', max_length=10)

