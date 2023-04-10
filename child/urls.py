from child import  views
from django.urls import path
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("login/", views.CreateLogin.as_view(), name='login'),
    path("logout/", LogoutView.as_view(next_page = 'login'), name='logout'),
    path("register/", views.RegisterPage.as_view(), name='register'),

    path("", views.TodoList.as_view(), name='todolist'),
    path("task/<int:pk>/", views.TodoDetail.as_view(), name='tododetail'),
    path("tcreate", views.TodoCreate.as_view(), name='todocreate'),
    path("tupdate/<int:pk>/", views.TodoUpdate.as_view(), name='todoupdate'),
    path("tdelete/<int:pk>/", views.TodoDelete.as_view(), name='tododelete'),
]
