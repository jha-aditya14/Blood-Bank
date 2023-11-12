from django.shortcuts import render, redirect
from hospitalOperations.models import UserHos, HospitalLogin, HospitalDetails, HospitalBloodBanks, UserAdminHos
from django.utils import timezone
# Create your views here.


def table(request, user_id):
    hospitalLogins = HospitalLogin.objects.all()

    # Create a dictionary to store hospital details
    tableData = []
    L=[]

    # Iterate through each hospital login to fetch details
    for hospitalLogin in hospitalLogins:
        details = HospitalDetails.objects.filter(hos=hospitalLogin).first()
        bloodBank = HospitalBloodBanks.objects.filter(hos=hospitalLogin).first()
        
        if details and bloodBank:
            tableData.append({
                "hosId":hospitalLogin.id,
                "email": hospitalLogin.email,
                "hosName": hospitalLogin.HosName,
                "addressLine": details.addressLine,
                "locality": details.locality,
                "city": details.city,
                "state": details.state,
                "country": details.country,
                "postalCode": details.postal_code,
                "phone": details.phone_number,
                "location": details.location,
                "aPositive": bloodBank.A_Positive,
                "bPositive": bloodBank.B_Positive,
                "abPositive": bloodBank.AB_Positive,
                "oPositive": bloodBank.O_Positive,
                "aNegative": bloodBank.A_Negative,
                "bNegative": bloodBank.B_Negative,
                "abNegative": bloodBank.AB_Negative,
                "oNegative": bloodBank.O_Negative,
            })
        
        else:
            tableData.append({
                "hosId":hospitalLogin.id,
                "email": hospitalLogin.email,
                "hosName": hospitalLogin.HosName,
                "addressLine": details.addressLine,
                "locality": details.locality,
                "city": details.city,
                "state": details.state,
                "country": details.country,
                "postalCode": details.postal_code,
                "phone": details.phone_number,
                "location": details.location,
                "aPositive": "N/A",
                "bPositive": "N/A",
                "abPositive": "N/A",
                "oPositive": "N/A",
                "aNegative": "N/A",
                "bNegative": "N/A",
                "abNegative": "N/A",
                "oNegative": "N/A",
        })
               
                
    data = {
        "userId": user_id,
        "hospitalDetails": tableData,
    }

    return render(request, "table.html", context=data)

def requestForBlood(request, user_id):
    if request.method == "POST":
        hosName = str(request.POST.get("hosName"))
        bloodGroup = str(request.POST.get("bloodGroup"))
        units = str(request.POST.get("units"))
        hosId = str(request.POST.get("hosId"))
        latitude = str(request.POST.get("latitude"))
        longitude = str(request.POST.get("latitude"))
        message = str(request.POST.get("message"))
        
         # Retrieve the HospitalLogin instance based on hosId
        hospital_instance = HospitalLogin.objects.get(id=hosId)
        date = timezone.now()
        userHos = UserHos(
            hos=hospital_instance,  # Assign the hospital instance
            user_id=user_id,  # You can directly assign the user_id
            messageRequested=message,
            BloodInUnits=units,
            BloodGroupAloted=bloodGroup,
            location=f"{latitude}, {longitude}",
            date_of_sent=date
        )
        userHos.save()

        return redirect('table', user_id=user_id)
        
        
        
        
def adminTable(request, user_id):
    hospitalLogins = HospitalLogin.objects.all()
    
    # Create a dictionary to store hospital details
    tableData = []

    hosUser =  UserAdminHos.objects.filter(user_id=user_id) 
    ownhosName= HospitalLogin.objects.filter(id=hosUser[0].hos_id)
    # Iterate through each hospital login to fetch details
    for hospitalLogin in hospitalLogins:
        details = HospitalDetails.objects.filter(hos=hospitalLogin).first()
        bloodBank = HospitalBloodBanks.objects.filter(hos=hospitalLogin).first()
        if details and bloodBank:
            tableData.append({
                "hosId":hospitalLogin.id,
                "email": hospitalLogin.email,
                "hosName": hospitalLogin.HosName,
                "addressLine": details.addressLine,
                "locality": details.locality,
                "city": details.city,
                "state": details.state,
                "country": details.country,
                "postalCode": details.postal_code,
                "phone": details.phone_number,
                "location": details.location,
                "aPositive": bloodBank.A_Positive,
                "bPositive": bloodBank.B_Positive,
                "abPositive": bloodBank.AB_Positive,
                "oPositive": bloodBank.O_Positive,
                "aNegative": bloodBank.A_Negative,
                "bNegative": bloodBank.B_Negative,
                "abNegative": bloodBank.AB_Negative,
                "oNegative": bloodBank.O_Negative,
            })
        
        else:
            tableData.append({
                "hosId":hospitalLogin.id,
                "email": hospitalLogin.email,
                "hosName": hospitalLogin.HosName,
                "addressLine": details.addressLine,
                "locality": details.locality,
                "city": details.city,
                "state": details.state,
                "country": details.country,
                "postalCode": details.postal_code,
                "phone": details.phone_number,
                "location": details.location,
                "aPositive": "N/A",
                "bPositive": "N/A",
                "abPositive": "N/A",
                "oPositive": "N/A",
                "aNegative": "N/A",
                "bNegative": "N/A",
                "abNegative": "N/A",
                "oNegative": "N/A",
        })
    
    data = {
        "userId": user_id,
        "hospitalDetails": tableData,
        "ownHosName":str(ownhosName[0].HosName), 
    }

    return render(request, "adminTable.html", context=data)

def adminRequestForBlood(request, user_id):
    if request.method == "POST":
        hosName = str(request.POST.get("hosName"))
        bloodGroup = str(request.POST.get("bloodGroup"))
        units = str(request.POST.get("units"))
        hosId = str(request.POST.get("hosId"))
        latitude = str(request.POST.get("latitude"))
        longitude = str(request.POST.get("latitude"))
        message = str(request.POST.get("message"))
        
         # Retrieve the HospitalLogin instance based on hosId
        hospital_instance = HospitalLogin.objects.get(id=hosId)
        date = timezone.now()
        userHos = UserHos(
            hos=hospital_instance,  # Assign the hospital instance
            user_id=user_id,  # You can directly assign the user_id
            messageRequested=message,
            BloodInUnits=units,
            BloodGroupAloted=bloodGroup,
            location=f"{latitude}, {longitude}",
            date_of_sent=date
        )
        userHos.save()

        return redirect('adminTable', user_id=user_id)

def adminAddBloodData(request, user_id):
    if request.method == "POST":
        hosId = str(request.POST.get("hosId"))
        bloodGroup = str(request.POST.get("bloodGroup"))
        units = str(request.POST.get("units"))
        hospital_instance = HospitalLogin.objects.get(id=hosId)
        
        
        try:
            data = HospitalBloodBanks.objects.get(hos=hospital_instance)
            if bloodGroup == "A+":
                hospital_to_update = HospitalBloodBanks.objects.get(hos=hospital_instance)
                if data.A_Positive == "":
                    hospital_to_update.A_Positive = int(units)
                else:
                    hospital_to_update.A_Positive = int(units)+int(data.A_Positive)
                    if int(units)+int(data.A_Positive)< 0:
                        return redirect('adminTable', user_id=user_id)
                    else:
                        hospital_to_update.save()
            if bloodGroup == "B+":
                hospital_to_update = HospitalBloodBanks.objects.get(hos=hospital_instance)
                if data.B_Positive == "":
                    hospital_to_update.B_Positive = int(units)
                else:
                    if int(units)+int(data.B_Positive)< 0:
                        return redirect('adminTable', user_id=user_id)
                    else:
                        hospital_to_update.B_Positive = int(units)+int(data.B_Positive)
                hospital_to_update.save()
            if bloodGroup == "AB+":
                hospital_to_update = HospitalBloodBanks.objects.get(hos=hospital_instance)
                if data.AB_Positive == "":
                    hospital_to_update.AB_Positive = int(units)
                else:
                    if int(units)+int(data.AB_Positive)< 0:
                        return redirect('adminTable', user_id=user_id)
                    else:
                        hospital_to_update.AB_Positive = int(units)+int(data.AB_Positive)
                hospital_to_update.save()
            if bloodGroup == "O+":
                hospital_to_update = HospitalBloodBanks.objects.get(hos=hospital_instance)
                if data.O_Positive == "":
                    hospital_to_update.O_Positive = int(units)
                else:
                    if int(units)+int(data.O_Positive)< 0:
                        return redirect('adminTable', user_id=user_id)
                    else:
                        hospital_to_update.O_Positive = int(units)+int(data.O_Positive)
                hospital_to_update.save()
            if bloodGroup == "A-":
                hospital_to_update = HospitalBloodBanks.objects.get(hos=hospital_instance)
                if data.A_Negative == "":
                    hospital_to_update.A_Negative = int(units)
                else:
                    if int(units)+int(data.A_Negative)< 0:
                        return redirect('adminTable', user_id=user_id)
                    else:
                        hospital_to_update.A_Negative = int(units)+int(data.A_Negative)
                hospital_to_update.save()
            if bloodGroup == "B-":
                hospital_to_update = HospitalBloodBanks.objects.get(hos=hospital_instance)
                if data.B_Negative == "":
                    hospital_to_update.B_Negative= int(units)
                else:
                    if int(units)+int(data.B_Negative)< 0:
                        return redirect('adminTable', user_id=user_id)
                    else:
                        hospital_to_update.B_Negative = int(units)+int(data.B_Negative)
                hospital_to_update.save()
            if bloodGroup == "AB-":
                hospital_to_update = HospitalBloodBanks.objects.get(hos=hospital_instance)
                if data.B_Positive == "":
                    hospital_to_update.AB_Negative = int(units)
                else:  
                    if int(units)+int(data.AB_Negative)< 0:
                        return redirect('adminTable', user_id=user_id)  
                    else:
                        hospital_to_update.AB_Negative = int(units)+int(data.AB_Negative)
                hospital_to_update.save()
            if bloodGroup == "O-":
                hospital_to_update = HospitalBloodBanks.objects.get(hos=hospital_instance)
                if data.B_Positive == "":
                    hospital_to_update.O_Negative = int(units)
                else:
                    if int(units)+int(data.O_Negative)< 0:
                        return redirect('adminTable', user_id=user_id)
                    else:
                        hospital_to_update.O_Negative = int(units)+int(data.O_Negative)
                hospital_to_update.save()
        except HospitalBloodBanks.DoesNotExist:
            if bloodGroup == "A+":
                hosBloodBank = HospitalBloodBanks(
                    hos=hospital_instance,  # Assign the hospital instance
                    A_Positive=units,        
                )
                hosBloodBank.save()
            if bloodGroup == "B+":
                hosBloodBank = HospitalBloodBanks(
                    hos=hospital_instance,  # Assign the hospital instance
                    B_Positive=units,        
                )
                hosBloodBank.save()
            if bloodGroup == "AB+":
                hosBloodBank = HospitalBloodBanks(
                    hos=hospital_instance,  # Assign the hospital instance
                    AB_Positive=units,        
                )
                hosBloodBank.save()
            if bloodGroup == "O+":
                hosBloodBank = HospitalBloodBanks(
                    hos=hospital_instance,  # Assign the hospital instance
                    O_Positive=units,        
                )
            if bloodGroup == "A-":
                hosBloodBank = HospitalBloodBanks(
                    hos=hospital_instance,  # Assign the hospital instance
                    A_Negative=units,        
                )
                hosBloodBank.save()
            if bloodGroup == "AB-":
                hosBloodBank = HospitalBloodBanks(
                    hos=hospital_instance,  # Assign the hospital instance
                    AB_Negative=units,        
                )
                hosBloodBank.save()
            if bloodGroup == "B-":
                hosBloodBank = HospitalBloodBanks(
                    hos=hospital_instance,  # Assign the hospital instance
                    B_Negative=units,        
                )
                hosBloodBank.save()
            if bloodGroup == "O-":
                hosBloodBank = HospitalBloodBanks(
                    hos=hospital_instance,  # Assign the hospital instance
                    O_Negative=units,        
                )
                hosBloodBank.save()

        return redirect('adminTable', user_id=user_id)


        
        