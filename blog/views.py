from django.views.decorators.http import require_http_methods, require_GET
from django.shortcuts             import render, redirect
from django.db.models             import QuerySet 
from django.utils                 import timezone
from django.http                  import HttpRequest,HttpResponse, HttpResponseBadRequest
from django.http                  import HttpResponseForbidden, HttpResponseNotAllowed
from django.http                  import QueryDict

from .models          import Post
from .forms           import PostForm
from .                import constants


@require_GET
def get_post_list(request: HttpRequest):
	posts: QuerySet = Post.objects.filter(published_date__lte = timezone.now()).order_by('-published_date')
	
	return render(
		request, 'blog/post_list.html',
		{
			'posts' : posts,
			'MAX_POST_PREVIEW_TITLE_LEN' : constants.MAX_POST_PREVIEW_TITLE_LEN,
			'MAX_POST_PREVIEW_TEXT_LEN'  : constants.MAX_POST_PREVIEW_TEXT_LEN,
		}
	)


@require_GET
def get_post_detail(request: HttpRequest, pk: int):
	post: QuerySet = Post.objects.get(pk = pk)
	return render(request, 'blog/post_detail.html', {'post' : post})


@require_http_methods(['GET', 'POST'])
def post_create(request: HttpRequest):
	if not request.user.is_authenticated:
		# здесь лучше сделать редирект на страницу регистрации \ авторизации или увед.
		return HttpResponseForbidden()
	
	if request.POST:
		form = PostForm(request.POST, request.FILES) if request.FILES else PostForm(request.POST)
	
		if form.is_valid(): 
			post: Post = form.save(commit = False) # commit - сохранять сразу в БД? Нет, сначало добавим автора
			post.author = request.user
			post.publish()
			
			return redirect('post_detail', pk = post.pk)

		else:
			return render(
				request,
				'blog/post_edit.html',
				{
					'form': form,
					'post': post,
					'method': 'post'
				},
				status=400
			)

	
	
	form = PostForm()
	return render(request, 'blog/post_edit.html',
		{
			'form' : form,
			'method' : 'post'
   		}
	)

# Должно обрабатывать edit через PUT
@require_http_methods(['GET', 'PUT', 'DELETE', 'POST'])
def post_edit(request: HttpRequest, pk: int):
	if not request.user.is_authenticated:
		# здесь лучше сделать редирект на страницу регистрации \ авторизации или увед. о недостатке доступа.
		return HttpResponseForbidden()
	

	post = Post.objects.get(pk = pk)
	
	if request.method == 'GET':
		form = PostForm(instance = post)
		return render(request, 'blog/post_edit.html',
			{
				'form' : form,
				'post' : post,
			}
		)
	

	# Запрос должен делаться через PUT, но в моей разметке реализация поддерживает только POST
	elif request.method in ('POST', 'PUT'): # ↓ для текущей реализации
		put_data = QueryDict(request.body) if not request.POST else request.POST
		form = PostForm(put_data, request.FILES, instance = post) if request.FILES else PostForm(put_data, instance = post)

		if form.is_valid():
			updated_post: Post = form.save()
			return redirect('post_detail', pk = updated_post.pk)
		
		else:
			return render(request, 'blog/post_edit.html', {
                    'form': form,
                    'post': post,
                }, status = 400)

	elif request.method == 'DELETE':
		post.delete()
		return redirect('post_list')