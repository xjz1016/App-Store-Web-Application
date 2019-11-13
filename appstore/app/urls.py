from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name='app'
urlpatterns = [
    path('', views.AppView.as_view(), name='all'),
]