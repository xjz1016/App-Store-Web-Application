from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.template.loader import render_to_string

from app.models import *
# Create your views here.

class AppView(View):
    def get(self, request) :
        host = request.get_host()
        template_name = "app/app_list.html"
        return render(request, template_name)


class AppCreate(LoginRequiredMixin,CreateView):
    model = App
    fields = '__all__'
    success_url = reverse_lazy('app:all')

class AppUpdate(LoginRequiredMixin, UpdateView):
    model = App
    fields = '__all__'
    success_url = reverse_lazy('app:all')

class AppDelete(LoginRequiredMixin, DeleteView):
    model = App
    fields = '__all__'
    success_url = reverse_lazy('app:all')


class CategoryCreate(LoginRequiredMixin, CreateView):
    model = Category
    fields = '__all__'
    success_url = reverse_lazy('app:all')