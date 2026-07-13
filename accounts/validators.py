from django.contrib import messages
from .models import User

def validators_signup(data):
    firstname = data.get("firstname")
    lastname = data.get("lastname")
    email = data.get("email")
    password = data.get("password")
    confirm_password = data.get("confirm_password")
    accept = data.get("accept")

    errors = {}
    
    if not firstname:
        errors["firstname"] = "First name is required."
    
    if not lastname:
        errors["lastname"] = "Last name is required."

    if not email:
        errors["email"] = "Email is required."
    elif User.objects.filter(email=email).exists():
        errors["email"] = "Email already registered."

    if not password:
        errors["password"] = "Password is required."
    elif len(password) < 8:
        errors["password"] = "Password must be at least 8 characters."

    if password != confirm_password:
        errors["confirm_password"] = "Passwords do not match."

    if not accept:
        errors["accept"] = "Please accept Terms & Conditions."

    return errors


def validators_login(data):
    errors = {}

    email = data.get("email")
    password = data.get("password")

    if not email:
        errors["email"] = "Email is required."

    if not password:
        errors["password"] = "Password is required."

    return errors