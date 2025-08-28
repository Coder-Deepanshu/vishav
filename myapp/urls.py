from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.login,name='login'),
    path('LogOut/',views.logout,name='logout'),
    path('Admin-Dashboard/',views.dashboard,name='dashboard'),
    path('Employee-Dashboard/',views.dashboard1,name='dashboard1'),
    path('Add-Employee/',views.add_employee,name='add_employee'),
    path('Add-Admin/',views.add_admin,name='add_admin'),

    path('employees/', views.employee_list, name='employee_list'),
    path('employee/<int:pk>/', views.employee_detail, name='employee_detail'),
    path('employee/<int:pk>/delete/', views.delete_employee, name='delete_employee'),
    path('employee/<int:pk>/edit/', views.edit_employee, name='edit_employee'),

    path('admin-list/', views.admin_list, name='admin_list'),
    path('admin-list/<int:pk>/', views.admin_detail, name='admin_detail'),
    path('admin-list/<int:pk>/delete/', views.delete_admin, name='delete_admin'),
    path('admin-list/<int:pk>/edit/', views.edit_admin, name='edit_admin'),

    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('employee_dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('mark_attendance/', views.mark_attendance, name='mark_attendance'),

]