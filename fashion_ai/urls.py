from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
	path('', views.index, name='index'),
    path('start', views.start, name='start'),
    path('login', LoginView.as_view(template_name='fashion_ai/login.html'), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('home', views.home, name='home'),
    path('prompt', views.prompt, name='prompt'),
    path('select', views.select, name='select'),
    path('preview/<str:name>/<int:size>/<int:x>/<int:y>', views.preview, name='preview'),
    path('mydesign', views.mydesign, name='mydesign'),
    path('update_design/<int:id>', views.update_design, name='update_design'),
    path('delete_design/<int:id>', views.delete_design, name='delete_design'),
    path('gallery', views.gallery, name='gallery'),
    path('favorite', views.favorite, name='favorite'),

    path('data', views.data, name='data'),
    path('update_item/<int:id>', views.update_item, name='update_item'),
    path('delete_item/<int:id>', views.delete_item, name='delete_item'),
    path('stable',views.stable, name= 'stable'),
    path('collage',views.collage, name= 'collage'),
]