from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('signup/reviewer/', views.ReviewerSignUpView.as_view(), name='reviewer_signup'),
    path('signup/developer/', views.DeveloperSignUpView.as_view(), name='developer_signup'),
]