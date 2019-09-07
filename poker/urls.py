from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.home),
    path('login/', LoginView.as_view(template_name='poker/login.html'), name="login"),
    path('logout/', LogoutView.as_view(template_name='poker/logout.html'), name="logout"),
    path('register/', views.register, name="register"),
    path('profile/', views.view_profile, name="profile"),
    path('profile/edit/', views.edit_profile, name="edit_profile"),
    path('change-password/', views.change_password, name='change_password')
]
