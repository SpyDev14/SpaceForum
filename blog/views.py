from django.shortcuts import render
from django.db.models import QuerySet 
from django.utils     import timezone
from django.http      import HttpRequest

from .models          import Post

def post_list(request: HttpRequest):
	posts: QuerySet = Post.objects.filter(created_date__lte = timezone.now()).order_by('-created_date')
	return render(request, 'blog/post_list.html', {'posts': posts})
