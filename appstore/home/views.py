from django.shortcuts import render
from django.views import View
from django.conf import settings
from app.models import App
import random

# Create your views here.

# This is a little complex because we need to detect when we are
# running in various configurations

class HomeView(View):
    def get(self, request) :
        print(request.get_host())
        host = request.get_host()
        islocal = host.find('localhost') >= 0 or host.find('127.0.0.1') >= 0
        popular_apps = App.objects.all().order_by('-rating')[:6]
        recommended_apps = list(App.objects.all())
        random.shuffle(recommended_apps)
        recommended_apps = recommended_apps[:6]
        newrelease_apps = App.objects.all().order_by('-date_updated')[:6]
        context = {
            'installed' : settings.INSTALLED_APPS,
            'islocal' : islocal,
            'popular_apps': popular_apps,
            'recommended_apps': recommended_apps,
            'newrelease_apps': newrelease_apps,
        }
        return render(request, 'home/main.html', context)



class TopratedView(View):
    def get(self, request) :
        # host = request.get_host()
        template_name = "home/toprated_list.html"
        toprated_list = App.objects.all().order_by('-rating')
        ctx = {'toprated_list': toprated_list}
        return render(request, template_name, ctx)



class RecommendedView(View):
    def get(self, request) :
        # host = request.get_host()
        template_name = "home/recommended_list.html"
        recommended_list = list(App.objects.all())
        random.shuffle(recommended_list)
        ctx = {'recommended_list': recommended_list}
        return render(request, template_name, ctx)



class NewreleaseView(View):
    def get(self, request) :
        # host = request.get_host()
        template_name = "home/newrelease_list.html"
        newrelease_list = App.objects.all().order_by('-date_updated')
        ctx = {'newrelease_list': newrelease_list}
        return render(request, template_name, ctx)