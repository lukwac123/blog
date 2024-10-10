from django.urls import path
from . import views

app_name = 'blog'
url_patterns = [
    # Widoki posta
    path('', views.post_list, name='post_list'),
    path('<int:id>/', views.post_detail, name='post_detail'),
]