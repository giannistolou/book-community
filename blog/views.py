from django.shortcuts import render, get_object_or_404
from .models import BlogPost, Tag, Category, Author
# Create your views here.
def index(request):
	posts = BlogPost.objects.all()
	return render(request, 'blog.html', {'posts': posts})

def get_similar_posts(post):
    # Get posts from the same category
    similar_posts = BlogPost.objects.filter(category=post.category).exclude(id=post.id)
    
    if similar_posts.count() < 3:
        # If less than 3 posts, get posts with the same tags
        similar_posts = BlogPost.objects.filter(tags__in=post.tags.all()).exclude(id=post.id).distinct()
    
    if similar_posts.count() < 3:
        # If still less than 3 posts, get random posts
        similar_posts = BlogPost.objects.exclude(id=post.id).order_by('?')
    
    return similar_posts[:3]

def post(request, post_slug,):
    post = get_object_or_404(BlogPost, slug=post_slug)
    similar_posts = get_similar_posts(post)
    return render(request, 'post.html', {'post': post, 'similar_posts': similar_posts})

def posts_by_tag(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = BlogPost.objects.filter(tags=tag)
    return render(request, 'genericListPage.html', {'posts': posts, 'title': tag.name, 'hasHashtag': True})

def posts_by_author(request, author_slug):
    author = get_object_or_404(Author, slug=author_slug)
    posts = BlogPost.objects.filter(author=author)
    return render(request, 'genericListPage.html', {'posts': posts, 'title': author.name, "pageImage": author.image_url})

def posts_by_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    posts = BlogPost.objects.filter(category=category)
    return render(request, 'genericListPage.html', {'posts': posts, 'category': category.name})