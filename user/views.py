from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

# Create your views here.

def register(request):
    formobj = RegisterForm(request.POST or None)
    if formobj.is_valid():
        username = formobj.cleaned_data.get("username")
        password = formobj.cleaned_data.get("password")
        newuser = User(username=username)
        newuser.set_password(password)
        newuser.save()
        login(request, newuser)
        messages.success(request, "Kayıt işlemi başarılı.")
        return redirect("index")
    context = {
        "form": formobj
    }
    return render(request, "register.htm", context)

# Bu kod da aynı işi yapar
"""
    if request.method == "POST":
        formobj = RegisterForm(request.POST)
        if formobj.is_valid():
            username = formobj.cleaned_data.get("username")
            password = formobj.cleaned_data.get("password")
            newuser = User(username=username)
            newuser.set_password(password)
            newuser.save()
            login(request, newuser)
            return redirect("index")
        else:
            context = {
                "form": formobj
            }
            return render(request, "register.htm", context)
    else:
        formobj = RegisterForm()
        context = {
            "form": formobj
        }
        return render(request, "register.htm", context)
"""

def loginuser(request):
    formobj = LoginForm(request.POST or None)
    context = {
        "form": formobj
    }

    if formobj.is_valid():
        username = formobj.cleaned_data.get("username")
        password = formobj.cleaned_data.get("password")

        user = authenticate(username=username, password=password)

        if user is None:
            messages.info(request, "Kullanıcı Adı veya Parola hatalı!")
            return render(request, "login.htm", context)
        messages.success(request, "Giriş işlemi başarılı.")
        login(request, user)
        return redirect("index")
    return render(request, "login.htm", context)

def logoutuser(request):
    logout(request)
    messages.success(request, "Sistemden başarıyla çıkıldı")
    return redirect("index")
