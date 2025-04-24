from django.shortcuts import render
from django.http import HttpRequest

def post_list(request: HttpRequest):
	return render(request, 'blog/post_list.html')
