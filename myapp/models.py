from django.db import models

# Create your models here.
class Employee(models.Model):
     # Basic Info
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    employee_id=models.CharField(max_length=15,unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    qualification=models.CharField(max_length=50)

    # Experience & Joining
    experience = models.DecimalField(max_digits=4, decimal_places=1)  # e.g., 5.5 years
    date_of_joining = models.DateField()

    # Contact Info
    phone = models.CharField(max_length=15)
    other_phone_no = models.CharField(max_length=15,null=True)
    gender = models.CharField(max_length=10, choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ])
    birthday = models.DateField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    state_code = models.CharField(max_length=10,null=True)
    country = models.CharField(max_length=30, choices=[
    ('India', 'India'),
    ('USA', 'USA'),
    ('UK', 'UK'),
    ('Canada', 'Canada'),
    ('Australia', 'Australia'),
    ('Germany', 'Germany'),
    ('France', 'France'),
    ('Japan', 'Japan'),
    ('China', 'China'),
    ('Other', 'Other')
])

    # Category
    category = models.CharField(max_length=10, choices=[
        ('Genral', 'General'),
        ('BC(A)', 'BC(A)'),
        ('BC(B)', 'BC(B)'),
        ('SC', 'SC'),
        ('ST', 'ST'),
        ('Others', 'Others')
    ])

    # Nationality & Religion
    nationality = models.CharField(max_length=20, choices=[
        ('Indian', 'Indian'),
        ('NRI', 'NRI'),
        ('Other', 'Other')
    ])
    religion = models.CharField(max_length=20, choices=[
        ('Hindu', 'Hindu'),
        ('Muslim', 'Muslim'),
        ('Sikh', 'Sikh'),
        ('Christian', 'Christian'),
        ('Jain', 'Jain'),
        ('Buddhist', 'Buddhist'),
        ('Other', 'Other')
    ])

    # Identity Info
    adhar_no = models.BigIntegerField()
    pan_no = models.CharField(max_length=20)

    # Marital Status
    martial_status = models.CharField(max_length=15, choices=[
        ('married', 'Married'),
        ('unmarried', 'Unmarried')
    ], default='unmarried')
    username=models.EmailField()
    password=models.CharField(max_length=15,null=True)

    def _str_(self):
        return self.name


class Admin(models.Model):
     # Basic Info
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    admin_id=models.CharField(max_length=15,unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    qualification=models.CharField(max_length=50)

    # Experience & Joining
    experience = models.DecimalField(max_digits=4, decimal_places=1)  # e.g., 5.5 years
    date_of_joining = models.DateField()

    # Contact Info
    phone = models.CharField(max_length=15)
    other_phone_no = models.CharField(max_length=15,null=True)
    gender = models.CharField(max_length=10, choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ])
    birthday = models.DateField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    state_code = models.CharField(max_length=10,null=True)
    country = models.CharField(max_length=30, choices=[
    ('India', 'India'),
    ('USA', 'USA'),
    ('UK', 'UK'),
    ('Canada', 'Canada'),
    ('Australia', 'Australia'),
    ('Germany', 'Germany'),
    ('France', 'France'),
    ('Japan', 'Japan'),
    ('China', 'China'),
    ('Other', 'Other')
])

    # Category
    category = models.CharField(max_length=10, choices=[
        ('Genral', 'General'),
        ('BC(A)', 'BC(A)'),
        ('BC(B)', 'BC(B)'),
        ('SC', 'SC'),
        ('ST', 'ST'),
        ('Others', 'Others')
    ])

    # Nationality & Religion
    nationality = models.CharField(max_length=20, choices=[
        ('Indian', 'Indian'),
        ('NRI', 'NRI'),
        ('Other', 'Other')
    ])
    religion = models.CharField(max_length=20, choices=[
        ('Hindu', 'Hindu'),
        ('Muslim', 'Muslim'),
        ('Sikh', 'Sikh'),
        ('Christian', 'Christian'),
        ('Jain', 'Jain'),
        ('Buddhist', 'Buddhist'),
        ('Other', 'Other')
    ])

    # Identity Info
    adhar_no = models.BigIntegerField()
    pan_no = models.CharField(max_length=20)

    # Marital Status
    martial_status = models.CharField(max_length=15, choices=[
        ('married', 'Married'),
        ('unmarried', 'Unmarried')
    ], default='unmarried')
    username=models.EmailField()
    password=models.CharField(max_length=15,null=True)

    def _str_(self):
        return self.name

from django.utils import timezone
class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=10, choices=[
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('half_day', 'Half Day')
    ])
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        unique_together = ['employee', 'date']
    
    def __str__(self):
        return f"{self.employee.name} - {self.date} - {self.status}"
