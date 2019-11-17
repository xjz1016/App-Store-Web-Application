from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name='app'
urlpatterns = [
    path('', views.AppView.as_view(), name='all'),
    path('main/create/', views.AppCreate.as_view(), name='app_create'),
    path('lookup/create/', views.CategoryCreate.as_view(), name='category_create'),
]