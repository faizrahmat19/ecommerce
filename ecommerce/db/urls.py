# db/urls.py

from django.urls import path
from . import views, viewsAdmin, viewsPelanggan
from django.contrib.auth import views as auth_views
from .views import CustomPasswordResetView, CustomPasswordResetConfirmView

urlpatterns = [
    # Accounts 
    path('login/', views.login_view, name='login'),
    path('register/', views.signup_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard
    path('dashboard/admin/', viewsAdmin.admin, name='dashboard_admin'),
    path('dashboard/', viewsPelanggan.pelanggan, name='dashboard_pelanggan'),

    #Reset Password
    path('db/password/reset/', CustomPasswordResetView.as_view(template_name='db/password_reset.html'), name='password_reset'),
    path('db/reset/password/done/', auth_views.PasswordResetDoneView.as_view(template_name='db/password_reset_done.html'), name='password_reset_done'),
    path('db/password/reset/confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('db/password/reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='db/password_reset_complete.html'), name='password_reset_complete'),
    
]
