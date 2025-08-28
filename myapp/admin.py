from django.contrib import admin
from .models import Employee,Admin,Attendance

# Register your models here.
@admin.register(Employee)
class AddEmployee(admin.ModelAdmin):
    list_display = ('name','employee_id' )
    search_fields = ('name', )

@admin.register(Admin)
class AddAdmin(admin.ModelAdmin):
    list_display = ('name','admin_id' )
    search_fields = ('name', )

@admin.register(Attendance)
class AddAttendance(admin.ModelAdmin):
    list_display = ('employee','status' )
    search_fields = ('employee', )