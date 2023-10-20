from django.shortcuts import render, redirect
from hospitalOperations.models import UserHos, HospitalLogin, HospitalDetails, HospitalBloodBanks 
from django.utils import timezone
# Create your views here.


def table(request, user_id):
    hospitalLogins = HospitalLogin.objects.all()

    # Create a dictionary to store hospital details
    tableData = []

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

    data = {
        "userId": user_id,
        "hospitalDetails": tableData,
    }

    return render(request, "adminTable.html", context=data)

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

    data = {
        "userId": user_id,
        "hospitalDetails": tableData,
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
        
        
        