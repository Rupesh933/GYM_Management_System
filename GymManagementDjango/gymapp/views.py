from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import *

# Create your views here.

from django.contrib import messages
from django.utils import timezone


def home(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        message = request.POST.get("message")

        if name and email and mobile and message:
            Enquiry.objects.create(
                name=name, email=email, contact_info=mobile, message=message
            )
            messages.success(request, "Your Enquiry has been submitted successfully!")
            return redirect("home")  # Redirect to home page after submission
        else:
            messages.error(request, "Please fill in all fields")

    return render(request, "home.html")


def about(request):
    return render(request, "about.html")


from django.contrib.auth import authenticate, login, logout


def admin_login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if (
            user is not None and getattr(user, "role", None) == "ADMIN"
        ):  # Login only if user is valid AND role is ADMIN
            login(
                request, user
            )  # log the user in using Django's built-in login function
            messages.success(request, "Logged in successfully!")
            return redirect(
                "admin_dashboard"
            )  # Redirect to admin dashboard after successful login
        else:
            messages.error(request, "Invalid Credentials or not an Admin")
    return render(request, "adminLogin.html")


def admin_logout_view(request):
    logout(request)
    # or   request.session.flush()   # delete all session data
    messages.info(request, "Logged Out successfully!!")
    return redirect("home")


def admin_required(view_func):
    # Before letting anyone access the page, check if they are logged in AND are an ADMIN user, if not redirect them to admin login page with an error message
    def wrapper(request, *args, **kwargs):
        if (
            not request.user.is_authenticated
            or getattr(request.user, "role", None) != "ADMIN"
        ):  # check if user is not authenticated OR role is not ADMIN
            messages.error(request, "you must be an admin to access this page")
            return redirect("admin_login")
        return view_func(
            request, *args, **kwargs
        )  # if user is authenticated and role is ADMIN, then allow them to access the page

    return wrapper


# from django.contrib.auth.decorators import login_required
# @login_required(login_url='admin_login')
@admin_required
def admin_dashboard_view(request):
    return render(request, "admin_dashboard.html")


@admin_required
def admin_plans_list(request):
    plans = MemberShipPlan.objects.all().order_by("duration_months")
    print("plans: ", plans)
    return render(request, "admin_plans_list.html", {"plans": plans})


@admin_required
def admin_plan_form(request):
    if request.method == "POST":
        name = request.POST.get("name")
        duration_months = request.POST.get("duration_months")
        fee = request.POST.get("fee")
        description = request.POST.get("description")

        if name and duration_months and fee:
            MemberShipPlan.objects.create(
                name=name,
                duration_months=duration_months,
                fee=fee,
                description=description,
            )
            messages.success(request, "MemberShip plan added successfully")
            return redirect("admin_plans_list")
        else:
            messages.error(request, "Please fill in all required fields")
    return render(request, "admin_plans_form.html", {"mode": "add"})


@admin_required
def admin_plan_edit(request, plan_id):
    plan = MemberShipPlan.objects.get(id=plan_id)
    if request.method == "POST":
        name = request.POST.get("name")
        duration_months = request.POST.get("duration_months")
        fee = request.POST.get("fee")
        description = request.POST.get("description")

        if name and duration_months and fee:
            plan.name = name
            plan.duration_months = duration_months
            plan.fee = fee
            plan.description = description
            plan.save()
            messages.success(request, "Membership plan updated successfully!")
            return redirect("admin_plans_list")
        else:
            messages.error(request, "Please fill in the required fields")

    return render(request, "admin_plans_form.html", {"mode": "edit", "plan": plan})


@admin_required
def admin_plan_delete(request, plan_id):
    plan = get_object_or_404(
        MemberShipPlan, id=plan_id
    )  # get the plan object or return 404 if not found
    if request.method == "POST":
        plan.delete()
        messages.success(request, "MemberShip plan deleted successfully!")
    else:
        messages.error(request, "Invalid request method")
    return redirect("admin_plans_list")


@admin_required
def admin_trainers_list(request):
    trainers = Trainer.objects.all().order_by("name")
    return render(request, "admin_trainers_list.html", {"trainers": trainers})


@admin_required
def admin_trainers_add(request):
    if request.method == "POST":
        name = request.POST.get("name")
        mobile = request.POST.get("mobile")
        specialization = request.POST.get("specialization")
        shift_timings = request.POST.get("shift_timings")

        if name and mobile and specialization and shift_timings:
            Trainer.objects.create(
                name=name.title(),
                mobile=mobile,
                specialization=specialization.title(),
                shift_timings=shift_timings.title(),
            )
            messages.success(request, "Trainers added successfully")
            return redirect("admin_trainers_list")
        else:
            messages.error(request, "Please fill in the all required fields")
    return render(request, "admin_trainers_add_edit.html", {"mode": "add"})


@admin_required
def admin_trainers_edit(request, trainer_id):
    trainer_id = Trainer.objects.get(id=trainer_id)
    if request.method == "POST":
        name = request.POST.get("name")
        mobile = request.POST.get("mobile")
        specialization = request.POST.get("specialization")
        shift_timings = request.POST.get("shift_timings")

        if name and mobile and specialization and shift_timings:
            trainer_id.name = name.title()
            trainer_id.mobile = mobile
            trainer_id.specialization = specialization.title()
            trainer_id.shift_timings = shift_timings.title()
            trainer_id.save()
            messages.success(request, "Trainer updated successfully!!")
            return redirect("admin_trainers_list")
        else:
            messages.error(request, "Please fill in the required fields")
    return render(
        request,
        "admin_trainers_add_edit.html",
        {"mode": "edit", "trainer_id": trainer_id},
    )  # we are passing the trainer_id object to the template so that we can pre-fill the form with the existing data of the trainer


@admin_required
def admin_trainers_delete(request, trainer_id):
    trainer = Trainer.objects.get(id=trainer_id)
    if request.method == "POST":
        trainer.delete()
        messages.success(request, "Trainer deleted successfully")
        return redirect("admin_trainers_list")
    else:
        messages.error(request, "Invalid request method")
    return redirect("admin_trainers_list")


@admin_required
def admin_member_list(request):
    search = request.GET.get(
        "search", ""
    )  # get the search query from the URL parameters, if no search query is provided then set it to an empty string
    members = MemberProfile.objects.all().select_related("user", "plan")

    if search:
        members = members.filter(full_name__icontains=search)
    return render(
        request, "admin_member_list.html", {"members": members, "search": search}
    )


@admin_required
def admin_member_add(request):
    plans = MemberShipPlan.objects.all().order_by("duration_months")
    trainer = Trainer.objects.all().order_by("name")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        full_name = request.POST.get("full_name")
        mobile = request.POST.get("mobile")
        gender = request.POST.get("gender")
        age = request.POST.get("age")
        address = request.POST.get("address")
        join_date = request.POST.get("join_date") or timezone.now().date

        plan_id = request.POST.get("plan_id")
        trainer_id = request.POST.get("trainer_id")

        if User.objects.filter(username=username).exists():
            messages.error(
                request, "username already exists! please choose a different username"
            )
            return redirect("admin_member_add")

        # create a new user object using Django's built-in create_user method which automatically hashes the password and saves the user to the database
        user = User.objects.create_user(
            username=username, password=password, role="MEMBER"
        )

        # get the plan object based on the selected plan_id from the form, if no plan is selected then set it to None
        plan = MemberShipPlan.objects.get(id=plan_id) if plan_id else None
        print("plan: ", plan)
        trainer = Trainer.objects.get(id=trainer_id) if trainer_id else None
        print("plan: ", plan)

        MemberProfile.objects.create(
            user=user,
            full_name=full_name,
            mobile=mobile,
            age=age,
            gender=gender,
            address=address,
            join_date=join_date,
            plan=plan,
            trainer=trainer,
        )
        messages.success(request, "Member added successfully!!")
        return redirect("admin_member_list")
    return render(
        request,
        "admin_member_add_edit.html",
        {"plans": plans, "trainers": trainer, "mode": "add"},
    )


@admin_required
def admin_member_edit(request, member_id):
    member = MemberProfile.objects.get(id=member_id)
    trainer = Trainer.objects.all().order_by("name")
    plans = MemberShipPlan.objects.all().order_by("name")
    print("member: ", member, "trainer: ", trainer, "plans: ", plans)

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        mobile = request.POST.get("mobile")
        age = request.POST.get("age")
        gender = request.POST.get("gender")
        address = request.POST.get("address")
        join_date = request.POST.get("join_date") or member.join_date
        trainer_id = request.POST.get("trainer_id")
        plan_id = request.POST.get("plan_id")

        # Get the plan object based on the selected plan_id from the form, if no plan is selected then set it to None
        plan = MemberShipPlan.objects.get(id=plan_id) if plan_id else None
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
        messages.success(request, "Member updated successfully!!")
        return redirect("admin_member_list")
    return render(
        request,
        "admin_member_add_edit.html",
        {"member": member, "trainers": trainer, "plans": plans, "mode": "edit"},
    )


@admin_required
def admin_member_delete(request, member_id):
    member = get_object_or_404(MemberProfile, id=member_id)
    if request.method == "POST":
        user = member.user
        member.delete()
        if user:
            user.delete()
        messages.success(request, "Member deleted successfully")
    else:
        messages.error(request, "Invalid request method")
    return redirect("admin_member_list")


@admin_required
def check_username(request):
    username = request.GET.get("username", "").strip()
    exists = bool(username) and User.objects.filter(username=username).exists()
    return JsonResponse({"exists": exists})


@admin_required
def admin_attendance_list(request):
    search_member = request.GET.get("search-member", "").strip()
    search_date = request.GET.get("search-date", "").strip()

    attendances = Attendance.objects.select_related("member").order_by(
        "-date", "-time_in"
    )

    if search_member:
        attendances = attendances.filter(member__full_name__icontains=search_member)

    if search_date:
        attendances = attendances.filter(date=search_date)

    return render(
        request,
        "admin_attendance_list.html",
        {
            "attendances": attendances,
            "search_member": search_member,
            "search_date": search_date,
        },
    )


@admin_required
def admin_attendance_add(request):
    members = MemberProfile.objects.all().order_by("full_name")
    if request.method == "POST":
        member_id = request.POST.get("member_id")
        current_datetime = timezone.now()

        date = request.POST.get("date") or current_datetime.date()
        time_in = request.POST.get("time_in") or current_datetime.time()

        if not member_id:
            messages.error(request, "Please select a member")
            return redirect("admin_attendance_add")
        member = get_object_or_404(MemberProfile, id=member_id)
        attendance, created = (
            Attendance.objects.get_or_create(  # get_or_create will check if an attendance record already exists for the given member and date, if it exists then it will return that record, if not then it will create a new record with the provided data
                member=member, date=date, defaults={"time_in": time_in}
            )
        )
        if created:
            messages.success(request, "Attendance record added successfully!!")
        else:
            messages.info(
                request,
                "Attendance record already exists for this member on the selected date",
            )
        return redirect("admin_attendance_list")
    return render(
        request, "admin_attendance_add_edit.html", {"members": members, "mode": "add"}
    )


@admin_required
def admin_attendance_edit(request, attendance_id):
    attendance = get_object_or_404(Attendance, id=attendance_id)
    members = MemberProfile.objects.all().order_by("full_name")

    if request.method == "POST":
        member_id = request.POST.get("member_id")
        date = request.POST.get("date")
        time_in = request.POST.get("time_in")

        if not member_id:
            messages.error(request, "Please select a member")
            return redirect("admin_attendance_edit", attendance_id=attendance.id)

        member = get_object_or_404(MemberProfile, id=member_id)
        duplicate_exists = (
            Attendance.objects.filter(
                member=member,
                date=date,
            )
            .exclude(id=attendance.id)
            .exists()
        )

        if duplicate_exists:
            messages.error(
                request,
                "Attendance record already exists for this member on the selected date",
            )
            return redirect("admin_attendance_edit", attendance_id=attendance.id)

        attendance.member = member
        attendance.date = date
        attendance.time_in = time_in or None
        attendance.save()
        messages.success(request, "Attendance record updated successfully!!")
        return redirect("admin_attendance_list")

    return render(
        request,
        "admin_attendance_add_edit.html",
        {
            "attendance": attendance,
            "members": members,
            "mode": "edit",
        },
    )


@admin_required
def admin_attendance_delete(request, attendance_id):
    attendance = get_object_or_404(Attendance, id=attendance_id)
    if request.method == "POST":
        attendance.delete()
        messages.success(request, "Attendance record deleted successfully")
    else:
        messages.error(request, "Invalid request method")
    return redirect("admin_attendance_list")

# Equipment logic
@admin_required
def admin_equipment_list(request):
    equipments = Equipment.objects.all()
    print("equipments purchase dates: ", [eq.purchase_date for eq in equipments])
    return render(request, 'admin_equipment_list.html', {'equipments': equipments})

@admin_required
def admin_equipment_add(request):
    equipment = None
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        units = request.POST.get('units', '').strip()
        purchase_date = request.POST.get('purchase_date', '').strip() or timezone.now().date()
        price = request.POST.get('price', '').strip()

        if name and units and purchase_date and price:
            Equipment.objects.create(
                name=name,
                units=units,
                purchase_date=purchase_date,
                price=price
            )
            messages.success(request, 'Equipment added successfully!')
            return redirect('admin_equipment_list')
        else:
            equipment = {
                'name': name,
                'units': units,
                'purchase_date': purchase_date,
                'price': price,
            }
            messages.error(request, 'Please fill in all required fields')
    return render(request, 'admin_equipment_add_edit.html', {'equipment': equipment, 'mode': 'add'})

@admin_required
def admin_equipment_edit(request, equipment_id):
    equipment = get_object_or_404(Equipment, id=equipment_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        units = request.POST.get('units')
        price = request.POST.get('price')
        purchase_date = request.POST.get('purchase_date') or equipment.purchase_date

        if name and units and price:
            equipment.name = name
            equipment.units = units
            equipment.price = price
            equipment.purchase_date = purchase_date
            equipment.save()
            messages.success(request, 'Equipment Updated Successfully!')
            return redirect('admin_equipment_list')
        else:
            messages.error(request, 'Please fill in the all required field')
    return render(request, 'admin_equipment_add_edit.html', {'equipment':equipment, 'mode':'edit'})

@admin_required
def admin_equipment_delete(request, equipment_id):
    equipment = get_object_or_404(Equipment, id = equipment_id)
    if request.method == 'GET':
        equipment.delete()
        messages.success(request, 'Equipment deleted successfully!')
    else:
        messages.error(request, 'Envalid request method')
    return redirect('admin_equipment_list')

@admin_required
def admin_enquiry_list(request):
    enquirys = Enquiry.objects.all().order_by('name')
    return render(request, 'admin_enquiry_list.html', {'enquirys':enquirys})

@admin_required
def admin_enquiry_update_status(request, enquiry_id):
    if request.method == 'POST':
        status = request.POST.get('status')
        enquiry = Enquiry.objects.get(id=enquiry_id)

        if status in ['NEW', 'SEEN', 'RESOLVED']:
            enquiry.status = status
            enquiry.save()
            messages.success(request, 'Enquiry status updated!')
    return redirect('admin_enquiry_list')

def admin_enquiry_delete(request, enquiry_id):
    pass

@admin_required
def admin_workout_plan_list(request):
    workout_plan = WorkoutPlan.objects.select_related('member').all().order_by('-creation_at') # we are using select_related to fetch the related member data in the same query to optimize the database queries and improve performance when we access workout_plan.member.full_name in the template, and we are ordering the workout plans by creation date in descending order so that the most recent workout plans are shown first
    # filter
    if request.method == 'GET':
        member_id = request.GET.get('member_id')
        if member_id:
            workout_plan = workout_plan.filter(member_id=member_id) 
        members = MemberProfile.objects.all().order_by('full_name') # we are fetching all members to show in the filter dropdown in the template
        print('members: ', [mem.full_name for mem in members])
    return render(request, 'admin_workout_plan_list.html', {'workout_plan':workout_plan, 'members':members, 'selected_member_id': member_id})

@admin_required
def admin_workout_plan_add(request):
    members = MemberProfile.objects.all().order_by('full_name')
    if request.method == 'POST':
        member_id = request.POST.get('member_id')
        title = request.POST.get('title')
        description = request.POST.get('description')
        
        if not member_id or not title or not description:
            messages.error(request, 'Please select member and enter title for the workout plan')
            return redirect('admin_workout_plans_add')
        
        member = get_object_or_404(MemberProfile, id=member_id)
        WorkoutPlan.objects.create(
            member=member,
            title=title,
            description=description,
        )
        messages.success(request, 'Workout plan added successfully!')
        return redirect('admin_workout_plan_list')
    
    return render(
        request,
        'admin_workout_plan_add_edit.html',
        {'mode': 'add', 'members': members},
    )

@admin_required
def admin_workout_plan_edit(request, workout_plan_id):
    workout_plan = get_object_or_404(WorkoutPlan, id=workout_plan_id)
    members = MemberProfile.objects.all().order_by('full_name')

    if request.method == 'POST':
        member_id = request.POST.get('member_id') or workout_plan.member.id  # if member_id is not provided in the form, then keep the existing member_id of the workout plan
        title = request.POST.get('title')
        description = request.POST.get('description')

        if member_id and title and description:
            member = get_object_or_404(MemberProfile, id=member_id)
            workout_plan.member = member
            workout_plan.title = title
            workout_plan.description = description
            workout_plan.save()
            messages.success(request, 'Workout plan updated successfully!')
            return redirect('admin_workout_plan_list')
        else:
            messages.error(request, 'Please select member and enter title for the workout plan')
            return redirect('admin_workout_plan_edit', workout_plan_id=workout_plan.id)
    return render(request, 'admin_workout_plan_add_edit.html', {'mode': 'edit', 'workout_plan': workout_plan, 'members': members})

@admin_required
def admin_workout_plan_delete(request, workout_plan_id):
    plan = WorkoutPlan.objects.get(id=workout_plan_id)
    if request.method == 'POST':
        plan.delete()
        messages.success(request, 'Workout plan deleted successfully!')
    else:
        messages.error(request, 'Invalid request method')
    return redirect('admin_workout_plan_list')

@admin_required
def admin_payment_list(request):
    payments = Payment.objects.select_related('member').all().order_by('-payment_date')
    return render(request, 'admin_payment_list.html', {'payments': payments})