
from django.urls import path

from .views import ArticleCreate, ArticleDetail

urlpatterns = [
    path('articles/', ArticleCreate.as_view(), name='article-create'),
    path('articles/<int:pk>/', ArticleDetail.as_view(), name='article-list'),
]
