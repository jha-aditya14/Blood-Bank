from django.shortcuts import render, redirect
from login.models import UserLogin, UserDetails 
from django.contrib import messages
from datetime import timedelta
import datetime
from datetime import datetime as dt
from django.utils import timezone
from django.db.models.functions import TruncMonth
from django.db.models import Count
import random
from django.conf import settings
import re
from login.utility import get_location_info , emailCheck
import bcrypt
# Create your views here.

def adminSignIn(request):
    if request.method == "POST":
        uemail = request.POST.get("email")
        passw = request.POST.get("passw")
        lat_location = str(request.POST.get("latitude")) 
        long_location = str(request.POST.get("longitude"))

        try:
            user = UserLogin.objects.get(email=uemail, is_staff=True)
            user_input_password = passw.encode('utf-8')
            if bcrypt.checkpw(user_input_password, user.password):
                url = f"/{user.id}/dashboard/"
                UserDetails.objects.filter(user_id=user.id).update(
                   last_logined=timezone.now(),
                    last_logined_location=str(lat_location + "," + long_location)
                )
                return redirect(url)
            else:
                message = "Email or Password is wrong"
                return render(request, "admin-sign-in.html", context={"message": "Email or Password is wrong"})
        
        except UserLogin.DoesNotExist:
            message = "User Not Exists. You can create your account by signing up"
        
        return render(request, "admin-sign-in.html", context={"message": message})

    return render(request, "admin-sign-in.html")

def adminSignUp(request):
    return render(request, "admin-sign-up.html")