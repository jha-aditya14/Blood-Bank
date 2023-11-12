from django.shortcuts import render, redirect
from hospitalOperations.models import UserHos,HospitalLogin, UserAdminHos
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
    else:
        
        userHos.RequestApproved=False 
        userHos.save()
        
    return redirect('adminRequest', user_id=user_id)