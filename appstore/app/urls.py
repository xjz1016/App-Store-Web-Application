from django.urls import path, reverse_lazy
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
    path('app/<int:pk>/review', views.ReviewCreateView.as_view(), name='app_review_create'),
    path('search', views.search, name='search'),
    path('app/<int:pk>/update/', views.AppUpdate.as_view(), name='app_update'),
    path('app/<int:pk>/delete/', views.AppDelete.as_view(), name='app_delete'),
    path('review/<int:pk>/delete/', views.ReviewDeleteView.as_view(), name='review_delete'),
    path('review/<int:pk>/update/', views.ReviewUpdate.as_view(), name='review_update'),
]