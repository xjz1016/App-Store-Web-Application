from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name='app'
urlpatterns = [
    path('', views.AppView.as_view(), name='all'),
    path('main/create/', views.AppCreate.as_view(), name='app_create'),
    path('category/create/', views.CategoryCreate.as_view(), name='category_create'),
    path('language/creat/', views.LanguageCreate.as_view(), name='language_create'),
    path('ad_picture/<int:pk>', views.stream_file, name='ad_picture'),
]