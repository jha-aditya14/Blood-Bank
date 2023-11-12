from django.shortcuts import render, redirect
from login.models import UserLogin, UserDetails
from django.utils import timezone
from datetime import datetime
from django.contrib import messages
import bcrypt
import re
# Create your views here.

def profile(request, user_id):
    if request.method == "POST":
        firstname = str(request.POST.get("firstName"))
        lastname = str(request.POST.get("lastName"))
        bloodgroup = str(request.POST.get("bloodGroup"))
        user_name = str(request.POST.get("username"))
        DOB = str(request.POST.get("dob"))
        email_ = str(request.POST.get("email"))
        address = str(request.POST.get("address"))
        city_ = str(request.POST.get("city"))
        country_ = str(request.POST.get("country"))
        state_ = str(request.POST.get("state"))
        postalcode = str(request.POST.get("postalCode"))
        phone = str(request.POST.get("phone"))
        
        
        user_profile = UserLogin.objects.get(id=user_id)  

        if firstname != None:
            user_profile.first_name = firstname
        if lastname != None:
            user_profile.last_name = lastname
        if email_ != None:
            user_profile.email = email_
        if user_name != None:
            user_profile.username = user_name
        user_profile.updated_at = timezone.now()
        
        user_profile.save()
        
        user_data= UserDetails.objects.get(user_id=user_id)
        
        if city_ != None:
            user_data.city = city_
        if state_ != None:    
            user_data.state = state_
        if country_ != None:
            user_data.country = country_
        if postalcode != None:
            user_data.postal_code =postalcode
        if address != None:
            user_data.locality = address
        if phone != None:
            user_data.phone_number = phone
        if bloodgroup != None:
            user_data.blood_group = bloodgroup
        
        if DOB:
            try:
                dob_date = datetime.strptime(DOB, "%Y-%m-%d").date()
                user_data.dob = dob_date
            except ValueError:
                pass
        else:
            user_data.dob = None 
        
        user_data.save()
        
        return redirect("profile", user_id=user_id)

    userLogedDetail = UserLogin.objects.filter(id=user_id)
    for detail in userLogedDetail:
        firstName=detail.first_name
        lastName=detail.last_name
        email = detail.email
        username = detail.username
        img = detail.img
    
    userDetail = UserDetails.objects.filter(user_id=user_id)
    for i in userDetail:
        bloodGroup = i.blood_group
        city = i.city
        state = i.state
        country = i.country
        postalCode = i.postal_code
        phone = i.phone_number
        locality = i.locality
        dob = i.dob
    formatted_dob = None
    if dob != None:
        formatted_dob = datetime.strptime(str(dob), "%Y-%m-%d").strftime("%Y-%m-%d")

    age=""
    messages.get_messages(request)  
    data={
        "userId":user_id,
        "firstName" : firstName,
        "lastName" : lastName,
        "email" : email,
        "username" : username,
        "img" : img,
        "bloodGroup" : bloodGroup,
        "city" : city,
        "state" : state,
        "country" : country,
        "postalCode" : postalCode,
        "phone" : phone,
        "locality" : locality,
        "dob" : formatted_dob,
        "age": age,
    }
    return render(request, "profile.html", context=data)

def profileImageUpdate(request, user_id):
    if request.method == "POST":
        image = request.FILES.get("image")
        user = UserLogin.objects.get(id=user_id)

        if image is None:
            image = user.img

        user.img = image
        user.updated_at = timezone.now()
        user.save()

    return redirect("profile", user_id=user_id)


def changePassword(request, user_id):
    if request.method == "POST":
        oldpasw = request.POST.get("oldpasw")
        newpasw = request.POST.get("newpasw")
        user = UserLogin.objects.get(id=user_id)
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        res = any(chr.isdigit() for chr in newpasw)
        uppercase = any(ele.isupper() for ele in newpasw)
        if oldpasw == newpasw:
            messages.success(request, "Old Password Entered iis Wrong")
            return redirect("profile", user_id=user_id)
        try:
            user = UserLogin.objects.get(id=user_id)
            user_input_password = oldpasw.encode('utf-8')
            if bcrypt.checkpw(user_input_password, user.password):
                if len(newpasw) < 8 or  regex.search(newpasw) == None or res == False or uppercase == False:
                    messages.success(request,"Password Should contain atleast 1 numeric character, 1 special character, 1 Uppercase character and alphabets with minimum length of 8 ")
                    return redirect("profile", user_id=user_id)   
                else:
                    password = newpasw.encode("utf-8")
                    salt = bcrypt.gensalt()
                    hashed_password = bcrypt.hashpw(password, salt)
                    user.password=hashed_password
                    user.updated_at =  timezone.now()
                    user.save()
                    messages.success(request, "Password changed successfully")
                    return redirect("profile", user_id=user_id)
            else:
                messages.success(request, "Old Password Entered is Wrong")
                return redirect("profile", user_id=user_id)
        except UserLogin.DoesNotExist:
            message = "User Not Exists. You can create your account by signing up"
        


        return redirect("profile", user_id=user_id)