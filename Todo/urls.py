from django.urls import path,include
from Todo import views
urlpatterns = [
    path('',views.home,name='my_task'),
    path('my_task_delete/<int:id>/',views.delete_task,name='my_task_delete'),
    path('complete/<int:id>/',views.complete_task,name='my_task_complete'),
    path('add_task/', views.add_task, name='my_task_add_task'),
]