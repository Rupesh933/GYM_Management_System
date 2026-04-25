from django.shortcuts import render, redirect
from .models import * 

# Create your views here.

from django.contrib import messages
def home(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        message = request.POST.get('message')

        if name and email and mobile and message:
            Enquiry.objects.create(name=name, email=email, contact_info=mobile, message=message)
            messages.success(request, 'Your Enquiry has been submitted successfully!')
            return redirect('home')  # Redirect to home page after submission
        else:
            messages.error(request, 'Please fill in all fields')
            
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

from django.contrib.auth import authenticate, login, logout
def admin_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and getattr(user, 'role', None) == 'ADMIN': # Login only if user is valid AND role is ADMIN
            login(request, user)   # log the user in using Django's built-in login function
            messages.success(request,'Logged in successfully!')
            return redirect('admin_dashboard')  # Redirect to admin dashboard after successful login
        else:
            messages.error(request, 'Invalid Credentials or not an Admin')
    return render(request, 'adminLogin.html')  

def admin_logout_view(request):
    logout(request)
    # or   request.session.flush()   # delete all session data
    messages.info(request, 'Logged Out successfully!!')
    return redirect('home')

def admin_required(view_func):
    # Before letting anyone access the page, check if they are logged in AND are an ADMIN user, if not redirect them to admin login page with an error message
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or getattr(request.user, 'role', None) != 'ADMIN':  # check if user is not authenticated OR role is not ADMIN
            messages.error(request, 'you must be an admin to access this page')
            return redirect('admin_login')
        return view_func(request, *args, **kwargs)  # if user is authenticated and role is ADMIN, then allow them to access the page
    return wrapper

# from django.contrib.auth.decorators import login_required
# @login_required(login_url='admin_login')
@admin_required
def admin_dashboard_view(request):
    return render(request, 'admin_dashboard.html')

@admin_required
def admin_plans_list(request):
    plans = MemberShipPlan.objects.all().order_by('duration_months')
    return render(request, 'admin_plans_list.html', {'plans': plans})

@admin_required
def admin_plan_form(request):
    if request.method=='POST':
        name = request.POST.get('name')
        duration_months = request.POST.get('duration_months')
        fee = request.POST.get('fee')
        description = request.POST.get('description')

        if name and duration_months and fee:
            MemberShipPlan.objects.create(
                name=name,
                duration_months=duration_months,
                fee=fee,
                description=description
            )
            messages.success(request, 'MemberShip plan added successfully')
            return redirect('admin_plans_list')
        else:
            messages.error(request, 'Please fill in all required fields')
        return render(request, 'admin_plans_form.html', {'mode':'add'})