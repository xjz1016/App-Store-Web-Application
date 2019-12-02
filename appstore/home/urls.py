from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home_page'),
    path('toprated', views.TopratedView.as_view(), name='toprated_app'),
    path('recommended', views.RecommendedView.as_view(), name='recommended_app'),
    path('newrelease', views.NewreleaseView.as_view(), name='newrelease_app'),
    path('category', views.CategoryView.as_view(), name='category_list'),
    path('category/<int:pk>', views.AppsPerCategoryView.as_view(), name='apps_per_category'),
    path('rank', views.RankView.as_view(), name='rank_list'),
    path('language', views.LanguageView.as_view(), name='language_list'),
    path('language/<int:pk>', views.AppsPerLanguageView.as_view(), name='apps_per_language'),
    # Uncomment this below if you have setup base_bootstrap.html and configured social login
    # path('accounts/login/', auth_views.LoginView.as_view(template_name=social_login)),
]

# The obtuse code below can be ignored - It dynamically switches
# between non-social login.html and social_login.html when we notice
# that social login has been configured in settings.py (later in the course)
# Or just uncomment the path above when you enable social login

app_name = 'home'
from django.conf import settings
try:
    if len(settings.SOCIAL_AUTH_GITHUB_KEY) > 0 :
        social_login = 'registration/login_social.html'
        urlpatterns += [
            path('accounts/login/', auth_views.LoginView.as_view(template_name=social_login)),
        ]
        print('Using',social_login,'as the login template for',settings.LOGIN_URL)
except:
    print('Using registration/login.html as the login template for',settings.LOGIN_URL)

# password_reset = 'registration/password_reset_form.html'
# urlpatterns += [
#      path('accounts/password_reset/', auth_views.PasswordResetView.as_view(template_name=password_reset)),
# ]