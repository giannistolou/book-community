from django.contrib import messages 
from django.shortcuts import redirect, render
from django.http import Http404
from django.conf import settings
from findBookCafe.models import Collection  
from blog.models import BlogPost
from .forms import SubscribeForm
import resend


resend.api_key = settings.RESEND_API_KEY
TURNSTILE_SECRET = settings.TURNSTILE_SECRET_KEY

def index(request):
    return render(request, 'landing-page.html')

def bio(request):
	latest_collections = Collection.objects.all().order_by('order_position')[:2]
	latest_posts = BlogPost.objects.order_by('-published_at')[:2]
	
	return render(request, 'bio.html', {
        'latest_collections': latest_collections,
        'latest_posts': latest_posts,
    })

def thank_you_subscribe(request):
    return render(request, 'thank-you-subscribe.html')
   

def subscribe(request):
    subscribe_form = SubscribeForm(request.POST or None)

    if request.method == "POST":
        if subscribe_form.is_valid():
            email = subscribe_form.cleaned_data['email']
            honeypot = subscribe_form.cleaned_data['honeypot']
            token = request.POST.get('cf-turnstile-response')

            import requests
            resp = requests.post('https://challenges.cloudflare.com/turnstile/v0/siteverify', 
                                data={'secret': TURNSTILE_SECRET, 'response': token})
            
            if not resp.json().get('success'):
                messages.error(request, "Captcha failed.")
                return render(request, "subscribe-newsletter.html", {'subscribe_form': subscribe_form})

            try:
                resend.Contacts.create({
                    "email": email,
                    "unsubscribed": False,                })
                messages.success(request, "Εγγραφή επιτυχής!")
                return redirect("thank_you_subscribe")
            except Exception as e:
                messages.error(request, f"Service error: {e}")
        else:
            messages.error(request, "Please correct the errors below.")

    return render(request, "subscribe-newsletter.html", {'subscribe_form': subscribe_form})
        