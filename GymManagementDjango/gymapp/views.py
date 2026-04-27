from django.shortcuts import render, redirect, get_object_or_404
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
    print('plans: ', plans)
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

@admin_required
def admin_plan_edit(request, plan_id):
    plan = MemberShipPlan.objects.get(id=plan_id)
    if request.method == "POST":
        name = request.POST.get('name')
        duration_months = request.POST.get('duration_months')
        fee = request.POST.get('fee')
        description = request.POST.get('description')

        if name and duration_months and fee:
            plan.name = name
            plan.duration_months = duration_months
            plan.fee = fee
            plan.description = description
            plan.save()
            messages.success(request, 'Membership plan updated successfully!')
            return redirect('admin_plans_list')
        else:
            messages.error(request, 'Please fill in the required fields')

    return render(request, 'admin_plans_form.html', {'mode': 'edit', 'plan': plan})

@admin_required
def admin_plan_delete(request, plan_id):
    plan = get_object_or_404(MemberShipPlan, id=plan_id)  # get the plan object or return 404 if not found
    if request.method == 'POST':
        plan.delete()
        messages.success(request, 'MemberShip plan deleted successfully!')
    else:
        messages.error(request, 'Invalid request method')
    return redirect('admin_plans_list')


@admin_required
def admin_trainers_list(request):
    trainers = Trainer.objects.all().order_by('name')
    return render(request, 'admin_trainers_list.html', {'trainers':trainers})

@admin_required
def admin_trainers_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        specialization = request.POST.get('specialization')
        shift_timings = request.POST.get('shift_timings')

        if name and mobile and specialization and shift_timings:
            Trainer.objects.create(
                name=name.capitalize(),
                mobile=mobile,
                specialization=specialization.capitalize(),
                shift_timings=shift_timings.capitalize()
            )
            messages.success(request, 'Trainers added successfully')
            return redirect('admin_trainers_list')
        else:
            messages.error(request, 'Please fill in the all required fields')
    return render(request, 'admin_trainers_add_edit.html', {'mode':'add'})

@admin_required
def admin_trainers_edit(request, trainer_id):
    trainer_id = Trainer.objects.get(id=trainer_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        specialization = request.POST.get('specialization')
        shift_timings = request.POST.get('shift_timings')

        if name and mobile and specialization and shift_timings:
            trainer_id.name = name.capitalize()  # capitalize the first letter of each word in the trainer's name before saving to database
            trainer_id.mobile = mobile
            trainer_id.specialization = specialization.capitalize()  # capitalize the first letter of each word in the specialization before saving to database
            trainer_id.shift_timings = shift_timings.capitalize() 
            trainer_id.save()
            messages.success(request, 'Trainer updated successfully!!')
            return redirect('admin_trainers_list')
        else:
            messages.error(request, 'Please fill in the required fields')
    return render(request, 'admin_trainers_add_edit.html', {'mode':'edit', 'trainer_id':trainer_id})  # we are passing the trainer_id object to the template so that we can pre-fill the form with the existing data of the trainer

@admin_required
def admin_trainers_delete(request, trainer_id):
    trainer = Trainer.objects.get(id=trainer_id)
    if request.method == 'POST':
        trainer.delete()
        messages.success(request, 'Trainer deleted successfully')
        return redirect('admin_trainers_list')
    else:
        messages.error(request, 'Invalid request method')
    return redirect('admin_trainers_list')

@admin_required
def admin_member_list(request):
    members = MemberProfile.objects.all().select_related('user', 'plan')
    return render(request, 'admin_member_list.html', {'members':members})

@admin_required
def admin_member_add(request):
    plans = MemberProfile.objects.all().order_by('duration_months')
    trainer = Trainer.objects.all().order_by('name')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        full_name = request.POST.get('full_name')
        mobile = request.POST.get('mobile')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        address = request.POST.get('address')
        join_date = request.POST.get('join_date')  or timezone.now().date

        plan_id = request.POST.get('plan_id')
        trainer_id = request.POST.get('trainer_id')

        if User.objects.filter(username=username, password=password).exists():
            messages.error(request, 'username already exists! please choose a different username')
            return redirect('admin_member_add')

        # create a new user object using Django's built-in create_user method which automatically hashes the password and saves the user to the database
        user = User.objects.create_user(    
                username=username,
                password=password,
                role='MEMBER'
                )  
        
        # get the plan object based on the selected plan_id from the form, if no plan is selected then set it to None
        plan = MemberShipPlan.objects.get(id=plan_id) if plan_id else None  
        print('plan: ',plan)
        trainer = Trainer.objects.get(id=trainer_id) if trainer_id else None
        print('plan: ',plan)

        MemberProfile.objects.create(
            user = user,
            full_name=full_name,
            mobile=mobile,
            age=age,
            gender=gender,
            address=address,
            join_date=join_date,
            plan=plan,
            trainer=trainer
        )
        messages.success(request, 'Member added successfully!!')
        return redirect('admin_member_list')
    return render(request, 'admin_member_add_edit.html', {'plans':plans, 'trainers':trainer, 'mode':'add'})


@admin_required
def admin_member_edit(request, member_id):
    member = MemberProfile.objects.get(id=member_id)
    trainer = Trainer.objects.all().order_by('duration_months')
    plans = MemberProfile.objects.all().order_by('name')
    print('member: ', member, 'trainer: ', trainer, 'plans: ',plans)

    if request.method == "POST":
        full_name = request.POST.get('full_name')
        mobile = request.POST.get('mobile')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        address = request.POST.get('address') 
        join_date = request.POST.get('join_date')  or member.join_date
        trainer_id = request.POST.get('trainer_id')
        plan_id = request.POST.get('plan_id')

        # Get the plan object based on the selected plan_id from the form, if no plan is selected then set it to None
        plan = MemberProfile.objects.get(id=plan_id) if plan_id else None
        trainer = Trainer.objects.get(id=trainer_id) if trainer_id else None 

        # Update the member profile with the new data from the form
        member.full_name = full_name
        member.mobile = mobile
        member.age = age
        member.gender = gender
        member.address = address
        member.join_date = join_date
        member.plan = plan
        member.trainer = trainer
        member.save()  # Save the updated member profile to the database
        messages.success(request, 'Member updated successfully!!')
        return redirect('admin_member_list')
    return render(request, 'admin_member_add_edit.html', {'member':member, 'trainers':trainer, 'plans':plans, 'mode':'edit'})

def admin_member_delete(request, member_id):
    pass