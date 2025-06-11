from django.shortcuts import render
from django.http import Http404
from findBookCafe.models import Collection  
from blog.models import BlogPost  

# Create your views here.
def index(request):
	return render(request, 'landing-page.html')

def bio(request):
	latest_collections = Collection.objects.all().order_by('order_position')[:2]
	latest_posts = BlogPost.objects.order_by('-published_at')[:2]
	
	return render(request, 'bio.html', {
        'latest_collections': latest_collections,
        'latest_posts': latest_posts,
    })