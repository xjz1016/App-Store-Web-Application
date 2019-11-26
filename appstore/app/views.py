from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse
from django.template.loader import render_to_string

from app.models import *
from app.forms import CreateForm, ReviewForm
from django.core import serializers
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
    success_url = reverse_lazy('home:home_page')
    def get(self, request, pk=None) :
        form = CreateForm()
        ctx = { 'form': form }
        return render(request, self.template, ctx)

    def post(self, request, pk=None) :
        form = CreateForm(request.POST, request.FILES or None)

        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template, ctx)

        # Add developer to the model before saving
        instance = form.save(commit=False)
        developer = get_object_or_404(Developer, developer_account=request.user)
        instance.developer = developer
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
        ctx = {'app': app, 'review_form': review_form, 'reviews': reviews, 'reviews_cnt': reviews_cnt, 'user': request.user}
        return render(request, self.template_name, ctx)


class AppUpdate(LoginRequiredMixin, UpdateView):
    template = 'app/app_form.html'
    success_url = reverse_lazy('accounts:profile_detail')
    def get(self, request, pk) :
        developer = get_object_or_404(Developer, developer_account=request.user)
        app = get_object_or_404(App, app_id=pk, developer=developer)
        form = CreateForm(instance=app)
        ctx = { 'form': form }
        return render(request, self.template, ctx)

    def post(self, request, pk=None) :
        developer = get_object_or_404(Developer, developer_account=request.user)
        app = get_object_or_404(App, app_id=pk, developer=developer)
        form = CreateForm(request.POST, request.FILES or None, instance=app)

        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template, ctx)

        app = form.save(commit=False)
        app.save()
        app_lan_deletes = get_list_or_404(App_to_language, app=app)
        for app_lan_delete in app_lan_deletes:
            app_lan_delete.delete()
        for language in form.cleaned_data['language']:
            App_to_language.objects.create(app=app, language=language)

        return redirect(self.success_url)

class AppDelete(LoginRequiredMixin, DeleteView):
    model = App
    template_name = 'app/app_delete.html'
    # fields = '__all__'
    success_url = reverse_lazy('accounts:profile_detail')


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
        f.rating = str((float(f.rating)+float(request.POST['rating']))/len(f.review_set.all()))
        f.save()
        return redirect(reverse('app:app_detail', args=[pk]))



class ReviewDeleteView(LoginRequiredMixin, View):
    model = Review
    template_name = 'app/review_delete.html'
    def get_success_url(self):
        app = self.object.app
        return reverse('app:app_detail', args=[app.app_id])
    # fields = '__all__'
    # success_url = reverse_lazy('accounts:profile_detail')

def search(request):
    q = request.GET.get('q')
    error_msg = ''

    if not q:
        error_msg = 'Please type in keywords'
        return render(request, 'app/result.html', {'error_msg': error_msg})

    app_list = App.objects.filter(app_name__icontains = q)
    return render(request, 'app/result.html', {'error_msg': error_msg, 'app_list': app_list})