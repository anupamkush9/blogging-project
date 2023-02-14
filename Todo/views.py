from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Task
def home(request):
    print("home function has been called.........")
    tasks=Task.objects.filter(user_id=request.user.id)
    print(tasks)
    return render(request,'Todo/home.html',{'tasks':tasks})

def delete_task(request,id):
    print("delete_task function has been called.........",id)
    Task.objects.get(id=id).delete()
    return redirect('/my_task')

def complete_task(request,id):
    comp=Task.objects.get(id=id)
    comp.complete= not comp.complete
    comp.save()
    return redirect('/my_task')

def add_task(request):
    if request.method=="POST":
        print("post request has come")
        title=request.POST.get('title')
        Task.objects.create(user_id=request.user,title=title)
        messages.success(request, 'Task Added Successfully !!')
        return redirect('/my_task')
    tasks=Task.objects.filter(user_id=request.user.id)
    print("in the add_task",tasks)
    return render(request,'Todo/home.html',{'tasks':tasks})
