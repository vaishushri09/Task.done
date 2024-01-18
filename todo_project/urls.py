"""
URL configuration for todo_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from todo_app.views import add_task,home,todo_list,generate_openai_response_view,create_room, room_detail, connect_to_room,inpp
from todo_app import views


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('todo_app.urls')),
    path('',views.home, name='home'),
    path('todo_list/',views.todo_list, name='todo_list'),
    # path('add/', views.add_task, name='add_task'),
    path('edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    # path('test_view/', views.test_view, name='test_view'),
    path('add_task/', views.add_task, name='add_task'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('all/', views.all_user_tasks, name='all_user_tasks'),
    path('register/', views.register, name='register'),
    path('mark_task_completed/<int:task_id>/', views.mark_task_completed, name='mark_task_completed'),
    path('sleep/', views.sleep_recommendation, name='sleep_recommendation'),
    path('generate_openai_response/', views.generate_openai_response_view, name='generate_openai_response'),
    path('create_room/', views.create_room, name='create_room'),
    path('room_detail/<int:room_id>/', views.room_detail, name='room_detail'),
    path('connect_to_room/', views.connect_to_room, name='connect_to_room'),
    path('inpp/',views.inpp,name='inpp'),
    path('room_detail/<int:room_id>/', views.room_detail, name='room_detail'),

]
