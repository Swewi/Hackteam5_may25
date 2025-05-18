from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.template.loader import render_to_string
from .forms import ContactForm
from .models import Contact


def contact(request):
    """
    View function to render the contact page with contact information.
    """
    if request.method == "POST":
        contact_form = ContactForm(data=request.POST)
        if contact_form.is_valid():
            contact = Contact(
                name=contact_form.cleaned_data['name'],
                email=contact_form.cleaned_data['email'],
                message=contact_form.cleaned_data['message'],
                read=False
            )
            contact.save()

            html = render_to_string('contact/email/contactform.html', {
                'name': contact_form.cleaned_data['name'],
                'email': contact_form.cleaned_data['email'],
                'message': contact_form.cleaned_data['message']
            })

            send_mail(
                'The contact form subject',
                'This is the message',
                'kireebellamy@gmail.com',
                ['kireebellamy@gmail.com'],
                html_message=html
            )

            messages.success(request, 'Success! Your message has been sent!')
            return redirect('contact')
    else:
        contact_form = ContactForm()

    return render(
        request,
        "contact/contact.html",
        {"contact_form": contact_form},
    )
