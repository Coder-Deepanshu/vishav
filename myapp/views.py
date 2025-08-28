from datetime import date, datetime
from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Employee

def login(request):
    role = request.POST.get('role')
    username = request.POST.get('username')
    password = request.POST.get('password')
    if role == 'admin':
        try:
            admin_username = Admin.objects.all().values_list('username', flat=True)
            admin_password = Admin.objects.all().values_list('password', flat=True)
            if username == 'Vishav' and password == 'AD20250':
                request.session['username'] = username
                request.session['adminid'] = password
                return render(request,'dashboard.html',{'username':username,'password':password})
            elif username in admin_username:
                if password in admin_password:
                    admin = Admin.objects.get(username = username)
                    request.session['username'] = admin.name
                    request.session['adminid'] = admin.admin_id
                    return render(request,'dashboard.html',{'username':admin.name})
                else:
                    messages.error(request, "Invalid admin credentials")
            else:
                messages.error(request, "Invalid admin credentials")
                return redirect('login')
        except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
                return redirect('login')
    elif role == 'employee':
        
        try:
            employee_username = Employee.objects.all().values_list('username', flat=True)
            employee_password = Employee.objects.all().values_list('password', flat=True)
            if username in employee_username:
                if password in employee_password:
                  employee = Employee.objects.get(username = username)
                  request.session['username1'] = employee.name
                  request.session['employeeid'] = employee.employee_id
                  return render(request,'dashboard1.html')
                else:
                    messages.error(request, "Invalid admin credentials")
                return redirect('login')

                 
        except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
                return redirect('login')
              
    return render(request,'login.html')

def logout(request):
    # Clear session data
    request.session.flush()
    return redirect('login')

from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import Employee
from django.utils.crypto import get_random_string
import re

def add_employee(request):
    if request.method == 'POST':
        # Extract all form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        father_name = request.POST.get('father_name')
        mother_name = request.POST.get('mother_name')
        position = request.POST.get('position')
        qualification = request.POST.get('qualification')
        experience = request.POST.get('experience')
        date_of_joining = request.POST.get('date_of_joining')
        phone = request.POST.get('phone')
        other_phone_no = request.POST.get('other_phone_no')
        gender = request.POST.get('gender')
        birthday = request.POST.get('birthday')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        state_code = request.POST.get('state_code')
        country = request.POST.get('country')
        category = request.POST.get('category')
        nationality = request.POST.get('nationality')
        religion = request.POST.get('religion')
        adhar_no = request.POST.get('adhar_no')
        pan_no = request.POST.get('pan_no')
        martial_status = request.POST.get('martial_status')
        
        # Basic validation
        if not all([name, email, father_name, mother_name, position, qualification, 
                   experience, date_of_joining, phone, gender, birthday, address, 
                   city, state, country, category, nationality, religion, adhar_no, 
                   pan_no, martial_status]):
            messages.error(request, "Please fill all required fields")
            return render(request, 'add_employee.html')
        
        # Email validation
        if Employee.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return render(request, 'add_employee.html')
        
        # Phone validation
        if not re.match(r'^\+?1?\d{9,15}$', phone):
            messages.error(request, "Invalid phone number format")
            return render(request, 'add_employee.html')
        
        # Aadhar validation (12 digits)
        if not re.match(r'^\d{12}$', adhar_no):
            messages.error(request, "Aadhar number must be 12 digits")
            return render(request, 'add_employee.html')
        
        # PAN validation (10 characters: 5 letters, 4 digits, 1 letter)
        if not re.match(r'^[A-Z]{5}\d{4}[A-Z]{1}$', pan_no.upper()):
            messages.error(request, "Invalid PAN number format")
            return render(request, 'add_employee.html')
        
        try:
            # Generate a unique employee ID
            employee_id = generate_employee_id()
            
            # Create the employee
            employee = Employee(
                name=name,
                email=email,
                father_name=father_name,
                mother_name=mother_name,
                position=position,
                qualification=qualification,
                experience=experience,
                date_of_joining=date_of_joining,
                phone=phone,
                other_phone_no=other_phone_no,
                gender=gender,
                birthday=birthday,
                address=address,
                city=city,
                state=state,
                state_code=state_code,
                country=country,
                category=category,
                nationality=nationality,
                religion=religion,
                adhar_no=adhar_no,
                pan_no=pan_no.upper(),
                martial_status=martial_status,
                employee_id=employee_id,
                # Set username as email and phone as password as per your requirement
                username=email,
                password=phone
            )
            
            employee.save()
            messages.success(request, f"Employee {name} added successfully with ID: {employee_id}")
            return redirect('add_employee')  # Redirect to clear form
            
        except Exception as e:
            messages.error(request, f"Error saving employee: {str(e)}")
            return render(request, 'add_employee.html')
    
    # GET request - show empty form
    return render(request, 'add_employee.html')

def generate_employee_id():
    """
    Generate a unique employee ID with format EMPXXXXX
    """
    prefix = "EMP"
    last_employee = Employee.objects.order_by('-id').first()
    
    if last_employee and last_employee.employee_id:
        try:
            last_id = int(last_employee.employee_id[3:])
            new_id = f"{prefix}{str(last_id + 1).zfill(5)}"
        except (ValueError, IndexError):
            new_id = f"{prefix}00001"
    else:
        new_id = f"{prefix}00001"
    
    # Ensure the ID is unique
    while Employee.objects.filter(employee_id=new_id).exists():
        numeric_part = int(new_id[3:]) + 1
        new_id = f"{prefix}{str(numeric_part).zfill(5)}"
    
    return new_id

# for admin
from .models import Admin
def add_admin(request):
    if request.method == 'POST':
        # Extract all form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        father_name = request.POST.get('father_name')
        mother_name = request.POST.get('mother_name')
        position = request.POST.get('position')
        qualification = request.POST.get('qualification')
        experience = request.POST.get('experience')
        date_of_joining = request.POST.get('date_of_joining')
        phone = request.POST.get('phone')
        other_phone_no = request.POST.get('other_phone_no')
        gender = request.POST.get('gender')
        birthday = request.POST.get('birthday')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        state_code = request.POST.get('state_code')
        country = request.POST.get('country')
        category = request.POST.get('category')
        nationality = request.POST.get('nationality')
        religion = request.POST.get('religion')
        adhar_no = request.POST.get('adhar_no')
        pan_no = request.POST.get('pan_no')
        martial_status = request.POST.get('martial_status')
        
        # Basic validation
        if not all([name, email, father_name, mother_name, position, qualification, 
                   experience, date_of_joining, phone, gender, birthday, address, 
                   city, state, country, category, nationality, religion, adhar_no, 
                   pan_no, martial_status]):
            messages.error(request, "Please fill all required fields")
            return render(request, 'add_admin.html')
        
        # Email validation
        if Admin.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return render(request, 'add_admin.html')
        
        # Phone validation
        if not re.match(r'^\+?1?\d{9,15}$', phone):
            messages.error(request, "Invalid phone number format")
            return render(request, 'add_admin.html')
        
        # Aadhar validation (12 digits)
        if not re.match(r'^\d{12}$', adhar_no):
            messages.error(request, "Aadhar number must be 12 digits")
            return render(request, 'add_admin.html')
        
        # PAN validation (10 characters: 5 letters, 4 digits, 1 letter)
        if not re.match(r'^[A-Z]{5}\d{4}[A-Z]{1}$', pan_no.upper()):
            messages.error(request, "Invalid PAN number format")
            return render(request, 'add_admin.html')
        
        try:
            # Generate a unique employee ID
            admin_id = generate_admin_id()
            
            # Create the employee
            admin = Admin(
                name=name,
                email=email,
                father_name=father_name,
                mother_name=mother_name,
                position=position,
                qualification=qualification,
                experience=experience,
                date_of_joining=date_of_joining,
                phone=phone,
                other_phone_no=other_phone_no,
                gender=gender,
                birthday=birthday,
                address=address,
                city=city,
                state=state,
                state_code=state_code,
                country=country,
                category=category,
                nationality=nationality,
                religion=religion,
                adhar_no=adhar_no,
                pan_no=pan_no.upper(),
                martial_status=martial_status,
                admin_id=admin_id,
                # Set username as email and phone as password as per your requirement
                username=email,
                password=phone
            )
            
            admin.save()
            messages.success(request, f"Admin {name} added successfully with ID: {admin_id}")
            return redirect('add_admin')  # Redirect to clear form
            
        except Exception as e:
            messages.error(request, f"Error saving admin: {str(e)}")
            return render(request, 'add_admin.html')
    
    # GET request - show empty form
    return render(request, 'add_admin.html')

def generate_admin_id():
    """
    Generate a unique employee ID with format EMPXXXXX
    """
    prefix = "AD"
    last_admin = Admin.objects.order_by('-id').first()
    
    if last_admin and last_admin.admin_id:
        try:
            last_id = int(last_admin.admin_id[3:])
            new_id = f"{prefix}{str(last_id + 1).zfill(5)}"
        except (ValueError, IndexError):
            new_id = f"{prefix}00001"
    else:
        new_id = f"{prefix}00001"
    
    # Ensure the ID is unique
    while Admin.objects.filter(admin_id=new_id).exists():
        numeric_part = int(new_id[3:]) + 1
        new_id = f"{prefix}{str(numeric_part).zfill(5)}"
    
    return new_id



# for employee

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.db import models
from .models import Employee
# Employee list view
def employee_list(request):
    # Get all employees from the database
    employees = Employee.objects.all().order_by('name')
    
    # Handle search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        employees = employees.filter(
            models.Q(name__icontains=search_query) |
            models.Q(employee_id__icontains=search_query) |
            models.Q(position__icontains=search_query) |
            models.Q(email__icontains=search_query)
        )
    
    context = {
        'employees': employees,
        'employee_count': employees.count(),
        'search_query': search_query,
    }
    return render(request, 'employee_list.html', context)

# Employee detail view
def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'employee_detail.html', {'employee': employee})

# Delete employee view
def delete_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    
    if request.method == 'POST':
        employee.delete()
        messages.success(request, f'Employee {employee.name} has been deleted successfully.')
        return redirect('employee_list')
    
    return render(request, 'confirm_delete.html', {'employee': employee})

# Edit employee view
def edit_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    
    if request.method == 'POST':
        # Update the employee with form data
        employee.name = request.POST.get('name')
        employee.email = request.POST.get('email')
        employee.position = request.POST.get('position')
        employee.phone = request.POST.get('phone')
        employee.father_name = request.POST.get('father_name')
        employee.mother_name = request.POST.get('mother_name')
        employee.qualification = request.POST.get('qualification')
        employee.experience = request.POST.get('experience')
        employee.address = request.POST.get('address')
        employee.city = request.POST.get('city')
        employee.state = request.POST.get('state')
        employee.country = request.POST.get('country')
        
        # Save the changes
        employee.save()
        
        messages.success(request, f'Employee {employee.name} has been updated successfully.')
        return redirect('employee_detail', pk=employee.pk)
    
    return render(request, 'edit_employee.html', {'employee': employee})

# Dashboard view
def dashboard1(request):
    # Get some statistics for the dashboard
    total_employees = Employee.objects.count()
    recent_hires = Employee.objects.order_by('-date_of_joining')[:5]
    username = request.sesssion.get('username1')
    
    context = {
        'total_employees': total_employees,
        'recent_hires': recent_hires,
        'username':username
    }
    return render(request, 'dashboard.html', context)


# for admin
def admin_list(request):
    # Get all employees from the database
    admin = Admin.objects.all().order_by('name')
    
    # Handle search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        admin = admin.filter(
            models.Q(name__icontains=search_query) |
            models.Q(admin_id__icontains=search_query) |
            models.Q(position__icontains=search_query) |
            models.Q(email__icontains=search_query)
        )
    
    context = {
        'admins': admin,
        'admin_count': admin.count(),
        'search_query': search_query,
    }
    return render(request, 'admin_list.html', context)

# Employee detail view
def admin_detail(request, pk):
    admin = get_object_or_404(Admin, pk=pk)
    return render(request, 'admin_detail.html', {'admin': admin})

# Delete employee view
def delete_admin(request, pk):
    admin = get_object_or_404(Employee, pk=pk)
    
    if request.method == 'POST':
        admin.delete()
        messages.success(request, f'Admin {admin.name} has been deleted successfully.')
        return redirect('admin_list')
    
    return render(request, 'confirm_delete1.html', {'admin': admin})

# Edit employee view
def edit_admin(request, pk):
    admin = get_object_or_404(Admin, pk=pk)
    
    if request.method == 'POST':
        # Update the employee with form data
        admin.name = request.POST.get('name')
        admin.email = request.POST.get('email')
        admin.position = request.POST.get('position')
        admin.phone = request.POST.get('phone')
        admin.father_name = request.POST.get('father_name')
        admin.mother_name = request.POST.get('mother_name')
        admin.qualification = request.POST.get('qualification')
        admin.experience = request.POST.get('experience')
        admin.address = request.POST.get('address')
        admin.city = request.POST.get('city')
        admin.state = request.POST.get('state')
        admin.country = request.POST.get('country')
        
        # Save the changes
        admin.save()
        
        messages.success(request, f'Admin {admin.name} has been updated successfully.')
        return redirect('admin_detail', pk=admin.pk)
    
    return render(request, 'edit_admin.html', {'admin':admin})

# Dashboard view
def dashboard(request):
    # Get some statistics for the dashboard
    total_employees = Admin.objects.count()
    recent_hires = Admin.objects.order_by('-date_of_joining')[:5]
    username = request.session.get('username')
    
    context = {
        'total_employees': total_employees,
        'recent_hires': recent_hires,
        'username':username
    }
    return render(request, 'dashboard.html', context)


from .models import Attendance
def admin_dashboard(request):
    if 'adminid' not in request.session:
        return redirect('login')
    
    employees = Employee.objects.all()
    today = date.today()
    
    # Get today's attendance for all employees
    today_attendance = {}
    for employee in employees:
        try:
            att = Attendance.objects.get(employee=employee, date=today)
            today_attendance[employee.employee_id] = att.status
        except Attendance.DoesNotExist:
            today_attendance[employee.employee_id] = 'Not Marked'
    
    context = {
        'employees': employees,
        'today_attendance': today_attendance,
        'today': today
    }
    return render(request, 'admin_dashboard.html', context)

def mark_attendance(request):
    if 'adminid' not in request.session:
        return redirect('login')
    
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        status = request.POST.get('status')
        notes = request.POST.get('notes', '')
        
        try:
            employee = Employee.objects.get(employee_id=employee_id)
            today = date.today()
            
            # Check if attendance already exists for today
            attendance, created = Attendance.objects.get_or_create(
                employee=employee, 
                date=today,
                defaults={
                    'status': status,
                    'notes': notes,
                    'check_in': datetime.now().time() if status != 'absent' else None
                }
            )
            
            if not created:
                attendance.status = status
                attendance.notes = notes
                if status != 'absent' and not attendance.check_in:
                    attendance.check_in = datetime.now().time()
                attendance.save()
            
            messages.success(request, f"Attendance marked as {status} for {employee.name}")
        except Employee.DoesNotExist:
            messages.error(request, "Employee not found")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
    
    return redirect('admin_dashboard')

def employee_dashboard(request):
    if 'employeeid' not in request.session:
        return redirect('login')
    
    try:
        employee = Employee.objects.get(employee_id=request.session['employeeid'])
        
        # Get attendance for the current month
        today = date.today()
        start_date = date(today.year, today.month, 1)
        
        attendance_records = Attendance.objects.filter(
            employee=employee, 
            date__gte=start_date
        ).order_by('-date')
        
        # Calculate stats
        total_days = (today - start_date).days + 1
        present_days = attendance_records.filter(status='present').count()
        absent_days = attendance_records.filter(status='absent').count()
        late_days = attendance_records.filter(status='late').count()
        half_days = attendance_records.filter(status='half_day').count()
        
        context = {
            'employee': employee,
            'attendance_records': attendance_records,
            'stats': {
                'total_days': total_days,
                'present_days': present_days,
                'absent_days': absent_days,
                'late_days': late_days,
                'half_days': half_days,
                'attendance_percentage': round((present_days + (half_days * 0.5)) / total_days * 100, 2) if total_days > 0 else 0
            }
        }
        return render(request, 'employee_dashboard.html', context)
    except Employee.DoesNotExist:
        messages.error(request, "Employee not found")
        return redirect('login')

def logout(request):
    request.session.flush()
    return redirect('login')