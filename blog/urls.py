from django.urls import path
from .           import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	path('',                    views.get_post_list,   name = 'post_list'  ),
	path('post/<int:pk>/',      views.get_post_detail, name = 'post_detail'),
	path('post/create/',        views.post_create,     name = 'post_create'),
	path('post/<int:pk>/edit/', views.post_edit,       name = 'post_edit'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)