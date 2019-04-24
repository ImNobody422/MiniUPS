from django.conf.urls import include,url 
from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name='index'),
    path('login_user/',views.login_user,name='login_user'),
    path('logout_user/', views.logout_user, name = 'logout_user'),
    path('register/', views.register , name = 'register'),
    path('package/',views.track_pkg, name = 'track_pkg'),
    path('package/<int:user.id>/',views.all_pkg, name = 'all_pkg'),
    path('edit_dest',views.edit_dest,name = 'edit_dest'),
    path('save_dest',views.save_dest,name = 'save_dest'),
    path('edit_email/', views.edit_email , name = 'edit_email'),
    path('loading/', views.loading, name = 'loading'),
    path('out/', views.out, name = 'out'),
    path('arrive/', views.arrive, name = 'arrive'),
    # path('all_info/',views.all_info,name = 'all_info'),
    url(r'^$',views.index),
    
]