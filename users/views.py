from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User, Group
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from users import forms
from users.forms import UpdateUserForm


def user_page(request):
    return render(request, "user_home.html")


def specific_user(request, user_id):
    if request.user.is_authenticated:
        if request.method == "GET":
            user_profile = get_object_or_404(User, id=user_id)
            update_form = UpdateUserForm(
                initial={'first_name': user_profile.first_name, 'last_name': user_profile.last_name,
                         'email': user_profile.email, 'phone_number': user_profile.phone_number})
            group_list = [group.name for group in request.user.groups.all()]
            context = {
                "user_profile": user_profile,
                "group_list": group_list,
                "update_form": update_form
            }
            return render(request, "user_detail.html", context)
        elif request.method == "POST":
            update_form = UpdateUserForm(request.POST)
            if update_form.is_valid():
                user_profile = get_object_or_404(User, id=user_id)
                user_profile.first_name = update_form.cleaned_data['first_name']
                user_profile.last_name = update_form.cleaned_data['last_name']
                user_profile.email = update_form.cleaned_data['email']
                user_profile.phone_number = update_form.cleaned_data['phone_number']
                user_profile.save()  # Зберігаємо зміни
                messages.success(request, "User edited successfully")
                return redirect(f'/users/{request.user.id}/')
            else:
                return render(request, "user_detail.html", {"update_form": update_form})
        else:
            return render(request, "user_home.html")


def login_page(request):
    if request.method == "GET":
        form_login = forms.LoginForm()
        return render(request, "login.html", context={"form_login": form_login})
    else:
        form_login = forms.LoginForm(request.POST)
        if form_login.is_valid():
            username = form_login.cleaned_data["username"]
            password = form_login.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return render(request, "user_home.html", context={'is_authenticated': True})
        messages.error(request, "Invalid credentials")  # Виведення повідомлення про помилку
        return render(request, "login.html", {"form_login": form_login})


def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect("/login/")
    return HttpResponse("Please log in first")


def register_page(request):
    if request.method == "GET":
        register_form = forms.RegisterForm()
        return render(request, "register.html", {'register_form': register_form})
    else:
        register_form = forms.RegisterForm(request.POST)
        if register_form.is_valid():
            created_user = register_form.save()
            client_group = Group.objects.get(name="Client")
            created_user.groups.add(client_group)
            created_user.save()
            messages.success(request, "Registration successful! Please log in.")  # Повідомлення про успішну реєстрацію
            return render(request, "login.html")
        else:
            return render(request, "register.html", {'register_form': register_form})
