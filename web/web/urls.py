"""
URL configuration for web project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from taigaweb import views

urlpatterns = [
    # path('', views.register),
    path('', views.userChoose, name='choose'),
    path('startSession/<int:session_id>/', views.startSession, name='start_session_with_id'),
    path('toSession/<int:session_id>/', views.toSession, name='to_session'),
    path('createSession/', views.createSession, name='create_session'),
    path('userChoose/', views.userChoose, name='choose'),
    path('get-matrix/<str:session_id>/', views.get_matrix, name='get_matrix'),
    path('set-matrix/<str:session_id>/', views.set_matrix, name='set_matrix'),

    path('get-matrix-MY/<str:session_id>/', views.get_matrix_MY, name='get_matrix_MY'),
    path('set-matrix-MY/<str:session_id>/', views.set_matrix_MY, name='set_matrix_MY'),
]
