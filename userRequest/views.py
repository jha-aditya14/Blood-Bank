from django.shortcuts import render, redirect
from hospitalOperations.models import UserHos,HospitalLogin
# Create your views here.
def requestTable(request, user_id):
    userRequests = UserHos.objects.filter(user_id=user_id)
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
    
    return render(request, "requestTable.html", context=data)

def requestDelete(request, user_id, requestId):
    userRequestDelete = UserHos.objects.get(id=requestId)
    userRequestDelete.delete()
    return redirect('requestTable', user_id=user_id)
