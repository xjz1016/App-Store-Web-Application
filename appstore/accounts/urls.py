from django.urls import path
from . import views

app_name='accounts'
urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('signup/reviewer/', views.ReviewerSignUpView.as_view(), name='reviewer_signup'),
    path('signup/developer/', views.DeveloperSignUpView.as_view(), name='developer_signup'),
    path('profile/', views.ProfileView.as_view(), name='profile_detail'),
]