from django.shortcuts import render, redirect
from .models import UserLogin, UserDetails 
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
from .utility import get_location_info , emailCheck
import bcrypt

# Create your views here.

def signin(request):
    if request.method == "POST":
        uemail = request.POST.get("email")
        passw = request.POST.get("passw")
        lat_location = str(request.POST.get("latitude")) 
        long_location = str(request.POST.get("longitude"))

        try:
            user = UserLogin.objects.get(email=uemail, is_staff=False)
            user_input_password = passw.encode('utf-8')
            user_stored_password = user.password.tobytes()
            
            if bcrypt.checkpw(user_input_password, user_stored_password):
                url = f"/{user.id}/dashboard/"
                UserDetails.objects.filter(user_id=user.id).update(
                   last_logined=timezone.now(),
                    last_logined_location=str(lat_location + "," + long_location)
                )
                return redirect(url)
            else:
                message = "Email or Password is wrong"
                return render(request, "sign-in.html", context={"message": "Email or Password is wrong"})
        
        except UserLogin.DoesNotExist:
            message = "User Not Exists. You can create your account by signing up"
        
        return render(request, "sign-in.html", context={"message": message})

    return render(request, "sign-in.html")

def signup(request):
    message = {}
    if request.method == "POST":
        uemail = str(request.POST.get("email"))
        passw = str(request.POST.get("password"))
        fname = str(request.POST.get("fname"))
        lname = str(request.POST.get("lname"))
        lat_location = str(request.POST.get("latitude")) 
        long_location = str(request.POST.get("longitude"))
        username = str(uemail.split("@")[1]) + "." + lname+"."+fname+str(uemail.split("@")[0])
        city, state, postal, country = get_location_info(float(lat_location), float(long_location))
        # Create a new user
        checkEmail = emailCheck(uemail)
        password = passw.encode("utf-8")
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password, salt)
        try:
            user = UserLogin.objects.get(email=uemail)
            messages.error(request, "A user with this email already exists.")
            message = {"message": "A user with this email already exists."}
            return render(request, "sign-up.html", context=message)
        except UserLogin.DoesNotExist:
            # Handle the case where the user doesn't exist
            regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
            res = any(chr.isdigit() for chr in passw)
            uppercase = any(ele.isupper() for ele in passw)
            if fname == "" and lname == "" and uemail == "" and passw == "":
                message = {"message": "All Fields Required"}
                return render(request, "sign-up.html", context=message)  
            if fname == "":
                message = {"message": "First Name Required "}
                return render(request, "sign-up.html", context=message)  
            if lname == "":
                message = {"message": "Last Name Required "}
                return render(request, "sign-up.html", context=message)  
            if uemail == "":
                message = {"message": "Email Required "}
                return render(request, "sign-up.html", context=message)  
            if checkEmail == False:
                message = {"message": "Enter Valid Email"}
                return render(request, "sign-up.html", context=message)
            if passw == "":
                message = {"message": "Password Required "}
                return render(request, "sign-up.html", context=message)  
            if len(passw) < 8 or  regex.search(passw) == None or res == False or uppercase == False:
                message = {"message": "Password Should contain atleast 1 numeric character, 1 special character, 1 Uppercase character and alphabets with minimum length of 8 "}
                return render(request, "sign-up.html", context=message)                
                
            else:
                username = str(uemail.split("@")[1]) + "." + lname + "." + fname + "." + uemail.split("@")[0]
                user = UserLogin(
                    email=uemail,
                    first_name=fname,
                    last_name=lname,
                    date_joined=timezone.now(),
                    is_staff=False,
                    is_active=True,
                    username=username.lower(),
                    password = hashed_password
                )
                user.save()
                
                user = UserLogin.objects.get(email=uemail)
                userId = user.id
                
                userData = UserDetails(
                    user_id= userId,
                    location=str(lat_location+","+long_location),
                    city = city,
                    state = state,
                    postal_code = postal,
                    country = country 
                )
                
                userData.save()

                messages.success(
                    request,
                    f"You have successfully signed up. User Name is {username.lower()} ",
                )
                message = {
                    "message": f"You have successfully signed up. User Name is {username.lower()} "
                }
                return redirect("signin")
    return render(request, "sign-up.html")