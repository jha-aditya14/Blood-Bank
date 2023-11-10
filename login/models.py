from django.db import models
# Create your models here.

class UserLogin(models.Model):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=300, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    password = models.BinaryField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    img=models.ImageField(upload_to='pics', null=True)

class UserDetails(models.Model):
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    user = models.ForeignKey(UserLogin, on_delete=models.CASCADE)
    city = models.CharField(max_length=1500)
    state = models.CharField(max_length=1500)
    country = models.CharField(max_length=1500)
    postal_code = models.CharField(max_length=150)
    country_code =models.CharField(max_length=10)
    locality = models.CharField(max_length=1500)
    phone_number = models.CharField(max_length=15)
    blood_group = blood_group = models.CharField(max_length=4, choices=BLOOD_GROUP_CHOICES)
    location = models.CharField(max_length=1500)
    last_logined = models.DateTimeField(auto_now_add=True)
    last_logined_location = models.CharField(max_length=1500)
    updated_loction = models.CharField(max_length=1500)
    dob =models.DateField(null=True, blank=True)
    
    
