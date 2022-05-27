from django.urls import path
from . import views

urlpatterns = [
    path('', views.prompt),
    path('create/', views.create)
]
