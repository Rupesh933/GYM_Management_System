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
        user = authenticate(request, username=username, passowrd=password)
        if user is not None and getattr(user, 'role', None):  #
    return render(request, 'adminLogin.html')