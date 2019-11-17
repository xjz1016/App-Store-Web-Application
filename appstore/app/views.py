from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.template.loader import render_to_string

from app.models import *
from app.forms import CreateForm
# Create your views here.

class AppView(View):
    def get(self, request) :
        host = request.get_host()
        template_name = "app/app_list.html"
        return render(request, template_name)


class AppCreate(LoginRequiredMixin,CreateView):
    # model = App
    # fields = ['app_name', 'size', 'version', 'rating', 'category',
    # 'language']
    # success_url = reverse_lazy('app:all')
    template = 'app/app_form.html'
    success_url = reverse_lazy('app:all')
    def get(self, request, pk=None) :
        form = CreateForm()
        ctx = { 'form': form }
        return render(request, self.template, ctx)

    def post(self, request, pk=None) :
        form = CreateForm(request.POST, request.FILES or None)

        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template, ctx)

        # Add owner to the model before saving
        # ad = form.save(commit=False)
        # ad.owner = self.request.user
        # ad.save()
        return redirect(self.success_url)

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


class LanguageCreate(LoginRequiredMixin, CreateView):
    model = Language
    fields = ['language_name']
    success_url = reverse_lazy('app:all')


def stream_file(request, pk) :
    app = get_object_or_404(App, id=pk)
    response = HttpResponse()
    response['Content-Type'] = app.content_type
    response['Content-Length'] = len(app.picture)
    response.write(app.picture)
    return response