from django.urls import path
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('', views.home, name="home"),
    path('user/<str:pk>', views.profileUser, name="user"),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('upload/<str:pk>', views.temupload, name="upload"),
    path('share/<str:pk_title>', views.sharefile, name="share"),
    path('delete/<str:pk_title>', views.deletefile, name="delete"),
    path('sharedelete/<str:pk_title>', views.deleteshare, name="deleteshare"),
    path('download/<str:title>', views.downloads, name = "download"),
    path('adminprofile/<str:pk>', views.adminprofile, name = 'admin'),
    path('blockuser/<str:uid>', views.blockuser, name = 'blockuser'),
    path('activeuser/<str:uid>', views.activeuser, name = 'activeuser'),


    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='ddp/password_reset.html'),
         name='reset_password'),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name='ddp/password_reset_sent.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='ddp/password_reset_form.html'),
         name='password_reset_confirm'),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='ddp/password_reset_done.html')
         , name='password_reset_complete')

]