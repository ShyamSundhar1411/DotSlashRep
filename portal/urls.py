from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.portal,name = "portal"),
    #ToDos
    path('todos/',views.todos,name = "view_all_todos"),
    path('todo/create',views.ToDoCreateView.as_view(),name = "create_todo"),
    path('todo/<int:pk>/<slug:slug>/update',views.ToDoUpdateView.as_view(),name = "update_todo"),
    path("todo/<int:pk>/<slug:slug>/delete",views.deletetodo,name = "delete_todo"),
]