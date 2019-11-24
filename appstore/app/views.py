from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse
from django.template.loader import render_to_string

from app.models import *
from app.forms import CreateForm, ReviewForm
# Create your views here.

class AppListView(ListView):
    def get(self, request) :
        host = request.get_host()
        template_name = "app/app_list.html"
        app_list = App.objects.all()
        ctx = {'app_list': app_list}
        return render(request, template_name, ctx)


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
        instance = form.save(commit=False)
        instance.save()
        for language in form.cleaned_data['language']:
            App_to_language.objects.create(app=instance, language=language)
        return redirect(self.success_url)


class AppDetailView(LoginRequiredMixin, DetailView):
    model = App
    template_name = "app/app_detail.html"
    def get(self, request, pk) :
        app = App.objects.get(app_id=pk)
        review_form = ReviewForm()
        reviews = app.review_set.all().order_by('-date_updated')
        reviews_cnt = len(reviews)
        ctx = {'app': app, 'review_form': review_form, 'reviews': reviews, 'reviews_cnt': reviews_cnt}
        return render(request, self.template_name, ctx)


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
    # fields = '__all__'
    success_url = reverse_lazy('app:all')


def stream_file(request, pk) :
    app = get_object_or_404(App, app_id=pk)
    response = HttpResponse()
    response['Content-Type'] = app.content_type
    response['Content-Length'] = len(app.picture)
    response.write(app.picture)
    return response


class ReviewCreateView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        f = get_object_or_404(App, app_id=pk)
        reviewer = get_object_or_404(Reviewer, reviewer=request.user)
        review = Review(review_text=request.POST['review'], stars=request.POST['rating'], reviewer=reviewer, app=f)
        review.save()
        return redirect(reverse('app:app_detail', args=[pk]))