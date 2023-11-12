from django.shortcuts import render
from login.models import UserDetails, UserLogin
from hospitalOperations.models import UserHos, HospitalLogin, HospitalDetails, HospitalBloodBanks
from django.utils import timezone
from datetime import timedelta, datetime
from sqlalchemy import func
from django.db.models import Sum, Count, F, Subquery, OuterRef, DateField
from django.db.models.functions import TruncMonth
from django.db.models.functions import ExtractYear, ExtractMonth, TruncDate
    

# Create your views here.

def dashBoard(request, user_id):
    today = timezone.now().date()
    yesterday = timezone.now().date() - timedelta(days=1)
    
    # Count users who logged in yesterday and today
    user_count_logined_today = UserDetails.objects.filter(last_logined__date=today).count()
    user_count_logined_yesterday = UserDetails.objects.filter(last_logined__date=yesterday).count()
    
    # Calculate the percentage increase
    if user_count_logined_yesterday  == 0:
        percentage_increase_login = 100  # Handle the case where there were no logins yesterday
    else:
        percentage_increase_login = ((user_count_logined_today - user_count_logined_yesterday ) / user_count_logined_yesterday ) * 100
    # Count todats request
    request_count = UserHos.objects.filter(user_id=user_id, date_of_sent__date=today).count()
    # New Users Since Last Quater
    three_months_ago = timezone.now() - timedelta(days=90)
    # Get the current date
    current_date = datetime.now()
    # Calculate the last-to-last quarter start date
    last_to_last_quarter_start = current_date - timedelta(days=6 * 30)  # Assuming 30 days per month
    # Calculate the last-to-last quarter end date
    last_to_last_quarter_end = last_to_last_quarter_start + timedelta(days=89)  # Assuming 89 days in a quarter

    newUsers = UserLogin.objects.filter(date_joined__range=(three_months_ago, timezone.now())).count()
    usersJoinedbeforeQuater = UserLogin.objects.filter(date_joined__range=(last_to_last_quarter_end, last_to_last_quarter_start)).count()
    
    if usersJoinedbeforeQuater  == 0:
        percentage_increase_users = 100  # Handle the case where there were no logins yesterday
    else:
        percentage_increase_users = ((newUsers - usersJoinedbeforeQuater ) / usersJoinedbeforeQuater ) * 100
    #YourRequest
    yourRequest = UserHos.objects.filter(user_id=user_id).count()
    
    
    # current_year = timezone.now().year
    queryset = UserHos.objects.filter(
        user_id=8  # Filter by user_id
    ).values('date_of_approved').annotate(
        total_blood_in_ml=Sum('BloodInUnits')
    ).order_by('date_of_approved')
    
    dates = []
    unitBlood = []
    for i in queryset:
        dates.append(i["date_of_approved"])
        unitBlood.append(i["total_blood_in_ml"])
    months_list = [dt.month for dt in dates]
    
    month_names = [
    "Jan", "Feb", "Mar", "April",
    "May", "June", "July", "Aug",
    "Sept", "Oct", "Nov", "Dec"
    ]
    
    month_names_list = [month_names[month - 1] for month in months_list]    
    hospitalData = HospitalLogin.objects.all()
    hospitalName = {}

    for data in hospitalData:
        hospitalName[data.id] = data.HosName

    hospitalDetails = HospitalDetails.objects.all()
    hospitalDetail = {}

    for detail in hospitalDetails:
        hospitalDetail[detail.hos.id] = detail.addressLine + ", " + detail.locality + ", " + detail.city + ", " + detail.state + ", " + detail.country + ", " + detail.postal_code

    bloodGroupDetail = {}
    hospitalBloodGroup = HospitalBloodBanks.objects.all()

    for bg in hospitalBloodGroup:
        blood_groups = [(x.strip()) for x in bg.A_Positive.split(',') + bg.B_Positive.split(',') + bg.AB_Positive.split(',') + bg.O_Positive.split(',') + bg.A_Negative.split(',') + bg.B_Negative.split(',') + bg.AB_Negative.split(',') + bg.O_Negative.split(',')]
        bloodGroupDetail[bg.hos.id] = blood_groups

    combinedData = {}
    tableData=[]

    # Iterate through the hospital IDs
    for hos_id, hos_name in hospitalName.items():
        hospital_details = hospitalDetail.get(hos_id, "N/A")
        blood_group_info = bloodGroupDetail.get(hos_id, ["N/A"])
        # Create a list with the combined data for each hospital
        if blood_group_info[0] != "N/A":
            combinedData={"hosId":hos_id,
                "hosName":hos_name,
                "hosDetails":hospital_details,
                "aPos": blood_group_info[0],
                "bPos": blood_group_info[1],
                "abPos": blood_group_info[2],
                "oPos": blood_group_info[3],
                "aNeg": blood_group_info[4],
                "bNeg": blood_group_info[5],
                "abNeg": blood_group_info[6],
                "oNeg": blood_group_info[7],
            }
        
            tableData.append(combinedData)
        else:
            combinedData={"hosId":hos_id,
                "hosName":hos_name,
                "hosDetails":hospital_details,
                "aPos": "N/A",
                "bPos": "N/A",
                "abPos": "N/A",
                "oPos": "N/A",
                "aNeg": "N/A",
                "bNeg": "N/A",
                "abNeg": "N/A",
                "oNeg": "N/A",
            }
            tableData.append(combinedData)
    
    data = {
        "userId": user_id,
        "todayUsers" : user_count_logined_today,
        "UserLoginPercentage" : round(percentage_increase_login,2),
        "requestCount": request_count,
        "NewUsers":newUsers,
        "YourRequest":yourRequest,
        "PercentageIncreaseUser":percentage_increase_users,
        "months":month_names_list,
        "units":unitBlood,
        "tableData":tableData,
    }
    
    return render(request, "dashboard.html", context=data)

def adminDashBoard(request, user_id):
    today = timezone.now().date()
    yesterday = timezone.now().date() - timedelta(days=1)
    
    # Count users who logged in yesterday and today
    user_count_logined_today = UserDetails.objects.filter(last_logined__date=today).count()
    user_count_logined_yesterday = UserDetails.objects.filter(last_logined__date=yesterday).count()
    
    # Calculate the percentage increase
    if user_count_logined_yesterday  == 0:
        percentage_increase_login = 100  # Handle the case where there were no logins yesterday
    else:
        percentage_increase_login = ((user_count_logined_today - user_count_logined_yesterday ) / user_count_logined_yesterday ) * 100
    # Count todats request
    request_count = UserHos.objects.filter(user_id=user_id, date_of_sent__date=today).count()
    # New Users Since Last Quater
    three_months_ago = timezone.now() - timedelta(days=90)
    # Get the current date
    current_date = datetime.now()
    # Calculate the last-to-last quarter start date
    last_to_last_quarter_start = current_date - timedelta(days=6 * 30)  # Assuming 30 days per month
    # Calculate the last-to-last quarter end date
    last_to_last_quarter_end = last_to_last_quarter_start + timedelta(days=89)  # Assuming 89 days in a quarter

    newUsers = UserLogin.objects.filter(date_joined__range=(three_months_ago, timezone.now())).count()
    usersJoinedbeforeQuater = UserLogin.objects.filter(date_joined__range=(last_to_last_quarter_end, last_to_last_quarter_start)).count()
    
    if usersJoinedbeforeQuater  == 0:
        percentage_increase_users = 100  # Handle the case where there were no logins yesterday
    else:
        percentage_increase_users = ((newUsers - usersJoinedbeforeQuater ) / usersJoinedbeforeQuater ) * 100
    #YourRequest
    yourRequest = UserHos.objects.filter(user_id=user_id).count()
    
    
    # current_year = timezone.now().year
    queryset = UserHos.objects.filter(
        user_id=8  # Filter by user_id
    ).values('date_of_approved').annotate(
        total_blood_in_ml=Sum('BloodInUnits')
    ).order_by('date_of_approved')
    
    dates = []
    unitBlood = []
    for i in queryset:
        dates.append(i["date_of_approved"])
        unitBlood.append(i["total_blood_in_ml"])
    months_list = [dt.month for dt in dates]
    
    month_names = [
    "Jan", "Feb", "Mar", "April",
    "May", "June", "July", "Aug",
    "Sept", "Oct", "Nov", "Dec"
    ]
    
    month_names_list = [month_names[month - 1] for month in months_list]    
    hospitalData = HospitalLogin.objects.all()
    hospitalName = {}

    for data in hospitalData:
        hospitalName[data.id] = data.HosName

    hospitalDetails = HospitalDetails.objects.all()
    hospitalDetail = {}

    for detail in hospitalDetails:
        hospitalDetail[detail.hos.id] = detail.addressLine + ", " + detail.locality + ", " + detail.city + ", " + detail.state + ", " + detail.country + ", " + detail.postal_code

    bloodGroupDetail = {}
    hospitalBloodGroup = HospitalBloodBanks.objects.all()

    for bg in hospitalBloodGroup:
        blood_groups = [(x.strip()) for x in bg.A_Positive.split(',') + bg.B_Positive.split(',') + bg.AB_Positive.split(',') + bg.O_Positive.split(',') + bg.A_Negative.split(',') + bg.B_Negative.split(',') + bg.AB_Negative.split(',') + bg.O_Negative.split(',')]
        bloodGroupDetail[bg.hos.id] = blood_groups

    combinedData = {}
    tableData=[]

    # Iterate through the hospital IDs
    for hos_id, hos_name in hospitalName.items():
        hospital_details = hospitalDetail.get(hos_id, "N/A")
        blood_group_info = bloodGroupDetail.get(hos_id, ["N/A"])
        # Create a list with the combined data for each hospital
        if blood_group_info[0] != "N/A":
            combinedData={"hosId":hos_id,
                "hosName":hos_name,
                "hosDetails":hospital_details,
                "aPos": blood_group_info[0],
                "bPos": blood_group_info[1],
                "abPos": blood_group_info[2],
                "oPos": blood_group_info[3],
                "aNeg": blood_group_info[4],
                "bNeg": blood_group_info[5],
                "abNeg": blood_group_info[6],
                "oNeg": blood_group_info[7],
            }
        
            tableData.append(combinedData)
        else:
            combinedData={"hosId":hos_id,
                "hosName":hos_name,
                "hosDetails":hospital_details,
                "aPos": "N/A",
                "bPos": "N/A",
                "abPos": "N/A",
                "oPos": "N/A",
                "aNeg": "N/A",
                "bNeg": "N/A",
                "abNeg": "N/A",
                "oNeg": "N/A",
            }
            tableData.append(combinedData)
    
    data = {
        "userId": user_id,
        "todayUsers" : user_count_logined_today,
        "UserLoginPercentage" : round(percentage_increase_login,2),
        "requestCount": request_count,
        "NewUsers":newUsers,
        "YourRequest":yourRequest,
        "PercentageIncreaseUser":percentage_increase_users,
        "months":month_names_list,
        "units":unitBlood,
        "tableData":tableData,
    }

    return render(request, "adminDashboard.html", context=data)
