from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name='app'
urlpatterns = [
    path('', views.AppListView.as_view(), name='all'),
    path('app/create/', views.AppCreate.as_view(), name='app_create'),
    path('category/create/', views.CategoryCreate.as_view(), name='category_create'),
    path('language/create/', views.LanguageCreate.as_view(), name='language_create'),
    path('app_picture/<int:pk>', views.stream_file, name='app_picture'),
    path('app/<int:pk>', views.AppDetailView.as_view(), name='app_detail'),
]