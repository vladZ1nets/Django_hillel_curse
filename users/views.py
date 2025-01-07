from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User, Group
from django.shortcuts import render

def user_page(request):
    return render(request, "user_home.html")

def specific_user(request, user_id):
    user = User.objects.get(id=user_id)
    return render(request, "user_detail.html", {"user": user})

def login_page(request):
    if request.method == "GET":
        return render(request, "login.html")
    else:
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect("/")
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect("/login/")
    return HttpResponse("Please log in first")

def register_page(request):
    if request.method == "GET":
        return render(request, "register.html")
    else:
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
        client_group = Group.objects.get(name="Client")
        user.groups.add(client_group)
        user.save()
        return HttpResponseRedirect("/login/")

