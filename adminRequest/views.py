from django.shortcuts import render, redirect
from hospitalOperations.models import UserHos,HospitalLogin, UserAdminHos, HospitalBloodBanks
from django.utils import timezone

# Create your views here.

def adminRequest(request, user_id):
    adminHos = UserAdminHos.objects.filter(user_id=user_id)
    userRequests = UserHos.objects.filter(hos_id=adminHos[0].hos_id)
    tableData=[]
    userHosdata={}
    for i in userRequests:
        id=i.id
        message=i.messageRequested
        location=i.location
        dateOfSent=i.date_of_sent
        bloodInUnits=i.BloodInUnits
        if i.RequestApproved==None:
            RequestApproval = "Pending"
        if i.RequestApproved==True:
            RequestApproval = "Approved"
        if i.RequestApproved == False:
            RequestApproval = "Rejected"
        
        bloodGroupAloted = i.BloodGroupAloted
        
        if i.date_of_approved == None:
            dateOfApproved = "Not Approved Yet"  
        if i.date_of_approved !=None:
            dateOfApproved = i.date_of_approved
        
        hospName = HospitalLogin.objects.filter(id=i.hos.id)
        for i in hospName:
            hospitalName = i.HosName
                   
        userHosdata={
            "requestId":id,
            "user_id":user_id,
            "hosName":hospitalName,
            "message":message,
            "requestApproved":RequestApproval,
            "bloodInUnits":bloodInUnits,
            "bloodGroupAlloted":bloodGroupAloted,
            "location":location,
            "dateOfApproval": dateOfApproved,
            "dateOfSent":dateOfSent,   
        }
        tableData.append(userHosdata)
    
    data = {
        "userId":user_id,
        "tableData":tableData,
    }
    
    return render(request, "adminRequestTable.html", context=data)

def requestApproval(request, user_id, requestId):
    param_value = request.GET.get('param_name', None)
    today = timezone.now()
    userHos = UserHos.objects.get(id=requestId)
    if param_value == "accept":
        userHos.RequestApproved=True
        userHos.date_of_approved = today
        userHos.save()
        hospital_instance = HospitalLogin.objects.get(id=userHos.hos_id)
        
        
    
        data = HospitalBloodBanks.objects.get(hos=hospital_instance)
        if userHos.BloodGroupAloted == "A+":
            hospital_to_update = HospitalBloodBanks.objects.get(hos=hospital_instance)
        
            hospital_to_update.A_Positive = int(data.A_Positive)-int(userHos.BloodInUnits)
            if int(data.A_Positive)-int(userHos.BloodInUnits)< 0:
                return redirect('adminRequest', user_id=user_id)
            else:
                hospital_to_update.save()
        if userHos.BloodGroupAloted == "B+":
            hospital_to_update = HospitalBloodBanks.objects.get(hos=hospital_instance)
        
            hospital_to_update.B_Positive = int(data.B_Positive)-int(userHos.BloodInUnits)
            if int(data.B_Positive)-int(userHos.BloodInUnits)< 0:
                return redirect('adminRequest', user_id=user_id)
            else:
                hospital_to_update.save()
        if userHos.BloodGroupAloted == "AB+":
            hospital_to_update = HospitalBloodBanks.objects.get(hos=hospital_instance)
        
            hospital_to_update.AB_Positive = int(data.AB_Positive)-int(userHos.BloodInUnits)
            if int(data.AB_Positive)-int(userHos.BloodInUnits)< 0:
                return redirect('adminRequest', user_id=user_id)
            else:
                hospital_to_update.save()
        if userHos.BloodGroupAloted == "O+":
            hospital_to_update = HospitalBloodBanks.objects.get(hos=hospital_instance)
        
            hospital_to_update.O_Positive = int(data.O_Positive)-int(userHos.BloodInUnits)
            if int(data.O_Positive)-int(userHos.BloodInUnits)< 0:
                return redirect('adminRequest', user_id=user_id)
            else:
                hospital_to_update.save()
        if userHos.BloodGroupAloted == "A-":
            hospital_to_update = HospitalBloodBanks.objects.get(hos=hospital_instance)
        
            hospital_to_update.A_Negative = int(data.A_Negative)-int(userHos.BloodInUnits)
            if int(data.A_Negative)-int(userHos.BloodInUnits)< 0:
                return redirect('adminRequest', user_id=user_id)
            else:
                hospital_to_update.save()
        if userHos.BloodGroupAloted == "B-":
            hospital_to_update = HospitalBloodBanks.objects.get(hos=hospital_instance)
        
            hospital_to_update.B_Negative = int(data.B_Negative)-int(userHos.BloodInUnits)
            if int(data.B_Negative)-int(userHos.BloodInUnits)< 0:
                return redirect('adminRequest', user_id=user_id)
            else:
                hospital_to_update.save()
        if userHos.BloodGroupAloted == "AB-":
            hospital_to_update = HospitalBloodBanks.objects.get(hos=hospital_instance)
        
            hospital_to_update.AB_Negative = int(data.AB_Negative)-int(userHos.BloodInUnits)
            if int(data.AB_Negative)-int(userHos.BloodInUnits)< 0:
                return redirect('adminRequest', user_id=user_id)
            else:
                hospital_to_update.save()
        if userHos.BloodGroupAloted == "O-":
            hospital_to_update = HospitalBloodBanks.objects.get(hos=hospital_instance)
        
            hospital_to_update.O_Negative = int(data.O_Negative)-int(userHos.BloodInUnits)
            if int(data.O_Negative)-int(userHos.BloodInUnits)< 0:
                return redirect('adminRequest', user_id=user_id)
            else:
                hospital_to_update.save()
    else:
        userHos.RequestApproved=False 
        userHos.save()
        
    return redirect('adminRequest', user_id=user_id)