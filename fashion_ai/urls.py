from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
	path('', views.index, name='index'),
    path('start', views.start, name='start'),
    path('home', views.home, name='home'),
    path('select', views.select, name='select'),
    path('prompt', views.prompt, name='prompt'),
    path('preview', views.preview, name='preview'),
    path('original', views.original, name='original'),
    path('collection', views.collection, name='collection'),
    path('gallery', views.gallery, name='gallery'),
	path('generate_prompt', views.generate_prompt, name='generate_prompt'),
    path('login/', LoginView.as_view(template_name='fashion_ai/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
