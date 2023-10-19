from django.db import models
from login.models import UserLogin
# Create your models here.

class HospitalLogin(models.Model):
    email = models.EmailField(unique=True)
    hosUsername = models.CharField(max_length=30, unique=True)
    HosName = models.CharField(max_length=30)
    password = models.BinaryField()
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
class HospitalDetails(models.Model):
    hos = models.ForeignKey(HospitalLogin, on_delete=models.CASCADE)
    city = models.CharField(max_length=1500)
    state = models.CharField(max_length=1500)
    country = models.CharField(max_length=1500)
    addressLine = models.CharField(max_length=3000, default=None)
    postal_code = models.CharField(max_length=150)
    country_code =models.CharField(max_length=10)
    locality = models.CharField(max_length=1500)
    phone_number = models.CharField(max_length=15)
    location = models.CharField(max_length=1500)
    last_logined = models.DateTimeField(auto_now_add=True)
    last_logined_location = models.CharField(max_length=1500)
    updated_loction = models.CharField(max_length=1500)

class HospitalBloodBanks(models.Model):
    hos = models.ForeignKey(HospitalLogin, on_delete=models.CASCADE)
    A_Positive = models.CharField(max_length=90)
    B_Positive = models.CharField(max_length=90)
    AB_Positive = models.CharField(max_length=90)
    O_Positive = models.CharField(max_length=90)
    A_Negative = models.CharField(max_length=90)
    B_Negative = models.CharField(max_length=90)
    AB_Negative = models.CharField(max_length=90)
    O_Negative = models.CharField(max_length=90)
    
class UserHos(models.Model):
    hos = models.ForeignKey(HospitalLogin, on_delete=models.CASCADE)
    user = models.ForeignKey(UserLogin, on_delete=models.CASCADE)
    messageRequested = models.CharField(max_length=2000)
    RequestApproved = models.BooleanField(null=True)
    BloodInUnits = models.IntegerField()
    BloodGroupAloted = models.CharField(null=True)
    date_of_approved = models.DateTimeField(null=True)
    date_of_sent = models.DateTimeField(auto_now_add=False, default=None) 
    location=models.CharField(null=True)
