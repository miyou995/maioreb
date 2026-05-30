# Create your views here.
from django.http import HttpResponse

from .forms import NewsletterSubscriptionForm


def newsletter_subscribe(request):
    if request.method == "POST":
        form = NewsletterSubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(
                '<div class="newsletter-response success"><p class="text-white" >✓ Merci pour votre inscription !</p></div>'
            )
        else:
            return HttpResponse(
                '<div class="newsletter-response error"><p class="text-white">⚠ Email invalide ou déjà utilisé.</p></div>'
            )
    return HttpResponse(status=405)
