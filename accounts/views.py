from django.shortcuts import render, redirect
from .validators import validators_signup, validators_login
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .models import User
from shop.models import Order
from django.contrib.auth.decorators import login_required
import re

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

@login_required
def change_password(request):

    if request.method == "POST":
        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if not current_password or not new_password or not confirm_password:
            messages.error(request, "All fields are required.")
            return redirect("change_password")

        if not request.user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
            return redirect("change_password")
        
        if len(new_password) < 8:
            messages.error(request, "Password must be at least 8 characters.")
            return redirect("change_password")

        if not re.search(r"[A-Z]", new_password):
            messages.error(request, "Password must contain one uppercase letter.")
            return redirect("change_password")

        if not re.search(r"\d", new_password):
            messages.error(request, "Password must contain one number.")
            return redirect("change_password")

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", new_password):
            messages.error(request, "Password must contain one special character.")
            return redirect("change_password")

        if request.user.check_password(new_password):
            messages.error(request, "New password cannot be the same as current password.")
            return redirect("change_password")

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("change_password")

        
        request.user.set_password(new_password)
        request.user.save()

        update_session_auth_hash(request, request.user)

        messages.success(request, "Password changed successfully.")
        return redirect("change_password")

    return render(request, 'accounts/change-password.html', {})

@login_required
def my_orders(request):
    orders = (Order.objects.filter(user = request.user).prefetch_related("orderitem_set__product").order_by("-created_at"))

    return render(request, "accounts/my-orders.html", {"orders": orders})