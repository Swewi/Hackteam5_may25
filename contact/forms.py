from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(
        label="Full Name",
        max_length=200,
        widget=forms.TextInput(attrs={
            'placeholder': 'Please enter full name here',
            'aria-label': 'Full Name'
        })
    )
    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={
            'placeholder': 'Please enter a valid email here',
            'aria-label': 'Email Address'
        })
    )
    message = forms.CharField(
        label="Message",
        widget=forms.Textarea(attrs={
            'placeholder': 'Please enter your message here',
            'aria-label': 'Message'
        })
    )
    