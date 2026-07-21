from django.shortcuts import render, redirect
from .validators import validators_signup, validators_login
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import User
from django.contrib.auth.decorators import login_required

# Create your views here.

def signup(request):
    if request.method == "POST":

        data = request.POST
        errors = validators_signup(data)

        if errors:
            return render(
                request, "accounts/signup.html",
                {
                    "errors": errors,
                    "form_data": request.POST
                }
            )

        user = User.objects.create_user(
            first_name=data.get("firstname").strip(),
            last_name=data.get("lastname").strip(),
            username=data.get("email"),
            email=data.get("email"),
            password=data.get("password"),
        )
        messages.success(request, "Account created successfully.")
        return redirect("login")

    return render(request, "accounts/signup.html")


def login_view(request):
    if request.method == "POST":
        errors = validators_login(request.POST)

        if errors:
            return render(
                request,
                'accounts/login.html',
                {
                    "errors": errors,
                    "form_data" : request.POST
                }
            )

        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user is None:
            errors = {
                "invalid" : "Invalid credentials"
            }

            return render(
                request,
                'accounts/login.html',
                {
                    "errors": errors,
                    "form_data": request.POST
                }
            )
        login(request, user)
        return redirect("shopHome")
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def profile(request):
    user = request.user

    print("user", request.FILES)

    if request.method == "POST":
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.phone = request.POST.get("phone")

        if "profile_image" in request.FILES:
            user.profile_image = request.FILES["profile_image"]

        user.save()
        messages.success(request, "Profile updated successfully.")

        return redirect("profile")

    context = {
        'user' : user
    }
    return render(request, 'accounts/profile.html', context)

def forgot_password(request):
    return render(request, 'accounts/forgot-password.html')

def change_password(request):
    return render(request, 'accounts/change-password.html')