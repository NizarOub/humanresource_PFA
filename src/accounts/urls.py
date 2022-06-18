from django.urls import path
from .import views


app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('user/change-password/', views.changepassword, name='changepassword'),
    path('user/profile/view/', views.user_profile_view, name='userprofile'),


]
