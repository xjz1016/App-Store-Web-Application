from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from accounts.models import User
from django.contrib.auth import login
from django.shortcuts import redirect
from accounts.forms import ReviewerSignUpForm, DeveloperSignUpForm
from app.models import Reviewer
# Create your views here.

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class ReviewerSignUpView(generic.CreateView):
    model = User
    form_class = ReviewerSignUpForm
    template_name = 'signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'reviewer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home:home_page')


class DeveloperSignUpView(generic.CreateView):
    model = User
    form_class = DeveloperSignUpForm
    template_name = 'signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'developer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home:home_page')



class ProfileView(generic.CreateView):
    model = User
    def get(self, request) :
        host = request.get_host()
        template_name = "accounts/profile_detail.html"
        user = request.user
        reviewer = get_object_or_404(Reviewer, reviewer=user)
        reviews = reviewer.review_set.all().order_by('-date_updated')
        reviews_cnt = len(reviews)
        ctx = {'user': user, 'reviews': reviews, 'reviews_cnt': reviews_cnt}
        return render(request, template_name, ctx)