from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from .models import UserEditView
from .views import GoodbyeView 


urlpatterns = [
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('thank_you/', views.thank_you, name='thank_you'),
    path('', views.post_list, name='post_list'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('signup/', views.signup, name='signup'),
    path('create/', views.create_post, name='create_post'),
    path('post/<slug:slug>/delete/', views.delete_post, name='delete_post'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('3/password/', views.change_password_view, name='change_password'),
    path('blog/<slug:slug>/', views.post_detail, name='post_detail'),
    path('art/', views.art_category_view, name='art_category'),
    path('sport/', views.sport_category_view, name='sport_category'),
    path('logout/goodbye/', GoodbyeView.as_view(), name='goodbye'),
]
