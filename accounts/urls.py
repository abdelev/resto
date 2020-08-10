from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),

    path('menus/', views.menus, name='menus'),
    path('customer/<str:pk_test>', views.customer, name='customer'),

    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('user/', views.userPage, name="user-page"),
    path('account/', views.accountSettings, name="account"),

    path('create_order/<str:pk>', views.create_order, name='create_order'),
    path('update_order/<str:pk>', views.update_order,  name='update_order'),
    path('delete_order/<str:pk>', views.delete_order,  name='delete_order'),

    path('menus/create_menu/', views.create_menu, name='create_menu'),
    path('menus/update_menu/<str:pk>', views.update_menu, name='update_menu'),
    path('menus/delete_menu/<str:pk>', views.delete_menu, name='delete_menu'),

    path('stats/', views.stats, name='stats'),

    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
         name="reset_password"),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"),
         name="password_reset_complete"),

]