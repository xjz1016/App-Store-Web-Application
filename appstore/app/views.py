from django.shortcuts import render
from django.views import View
# Create your views here.

class AppView(View):
    def get(self, request) :
        host = request.get_host()
        template_name = "app/app_list.html"
        return render(request, template_name)