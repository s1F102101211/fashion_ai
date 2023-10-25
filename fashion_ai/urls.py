from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
	path('', views.index, name='index'),
	path('generate_prompt', views.generate_prompt, name='generate_prompt'),
    path('login/', LoginView.as_view(template_name='fashion_ai/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
