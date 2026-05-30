import os
from xml.dom.minidom import Document
from django.contrib import messages
from django.shortcuts import render




class HTMXFormMixin:
    def serve(self, request, *args, **kwargs):
        form = self.get_form(
            request.POST or None,
            request.FILES or None,
            page=self,
        )

        if request.method == "POST" and form.is_valid():
            self.process_form_submission(form)
            # HTMX request → return partial success
            if request.htmx:
                messages.success(request, "Message envoyé avec succès")
                return render(
                    request,
                    "snippets/success.html",
                    {"page": self},
                )
            # Normal request → fallback
            return render(  # TODO: we do not have this page for the moment if you need it make sure to create it
                request,
                "contact/thank_you.html",
                {"page": self},
            )

        return render(
            request,
            self.get_template(request, *args, **kwargs),
            {
                "page": self,
                "form": form,
            },
        )


    def process_form_submission(self, form):
        from django import forms
        from contact.models import ContactPage
        from recruitment.views import send_email_contact

        super().process_form_submission(form)
        cleaned_data =form.cleaned_data

        for name, field in form.fields.items():
            if isinstance(field, forms.FileField):
                uploaded_file = cleaned_data.get(name)
                if uploaded_file:
                    document = Document.objects.create(
                        title=os.path.basename(uploaded_file.name),
                        file=uploaded_file,
                        
                    )
                    # Store document ID or URL
                    cleaned_data[name] = self.request.build_absolute_uri(document.url) 
                else:
                    cleaned_data[name] = ""

        data = {}
        for name, field in form.fields.items():
            value = cleaned_data.get(name)
            
            if isinstance(field, forms.FileField) and value:
                data[name] = (
                self.request.build_absolute_uri(value.url)
                if hasattr(value, "url")
                else value)
            else:
                data[name] = value
        print("data------------------------->>>", data)

        contact_page = ContactPage.objects.first()
        if contact_page:
            recipients_emails = contact_page.get_recipient_list()
        else:
            recipients_emails = []
        print("recipients_emails------------------------->>>", recipients_emails)
        if recipients_emails:
            send_email_contact(
                self, recipients_emails, data=data,
            )