from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .models import User, Learner, Mentor, Booking, DietPlan
from django.utils import timezone
from datetime import datetime
from django.db.models import Sum
from django.contrib import messages

def home_view(request):
    return render(request, 'home.html')

def sign_up_selection_view(request):
    return render(request, 'sign.html')

def learner_signup_view(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        roll_number = request.POST.get('roll_number')
        goal = request.POST.get('goal')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, "Passwords do not match!")
            return redirect('lsignup')
        if User.objects.filter(email=email).exists():
            messages.error(request, "A user with this email already exists.")
            return redirect('lsignup')

        user = User.objects.create_user(username=email, email=email, password=password, role='learner', full_name=full_name)
        Learner.objects.create(user=user, roll_number=roll_number, goal=goal)
        login(request, user)
        return redirect('learner_dash')
    return render(request, 'lsign.html')

def mentor_signup_view(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        specialization = request.POST.get('specialization')
        experience = request.POST.get('experience')
        bio = request.POST.get('bio')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, "Passwords do not match!")
            return redirect('msign')
        if User.objects.filter(email=email).exists():
            messages.error(request, "A user with this email already exists.")
            return redirect('msign')
            
        user = User.objects.create_user(username=email, email=email, password=password, role='mentor', full_name=full_name)
        Mentor.objects.create(user=user, specialization=specialization, experience=experience, bio=bio)
        login(request, user)
        return redirect('mentor_dash')
    return render(request, 'msign.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            if user.role == 'learner':
                return redirect('learner_dash')
            elif user.role == 'mentor':
                return redirect('mentor_dash')
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('login_view')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def learner_dashboard_view(request):
    learner = request.user.learner
    recommended_mentors = Mentor.objects.filter(specialization__icontains=learner.goal.replace('_', ' ')).order_by('-points')[:3]
    context = {'learner': learner, 'recommended_mentors': recommended_mentors}
    return render(request, 'learner_dash.html', context)

@login_required
def mentor_dashboard_view(request):
    mentor = request.user.mentor
    upcoming_bookings = Booking.objects.filter(mentor=mentor, session_date__gte=timezone.now()).order_by('session_date')
    context = {'mentor': mentor, 'upcoming_bookings': upcoming_bookings}
    return render(request, 'mentor_dash.html', context)

@login_required
def booking_view(request):
    user = request.user
    now = timezone.now()
    if user.role == 'learner':
        upcoming_sessions = Booking.objects.filter(learner=user.learner, session_date__gte=now).order_by('session_date')
        completed_sessions = Booking.objects.filter(learner=user.learner, session_date__lt=now).order_by('-session_date')
    else: # Mentor
        upcoming_sessions = Booking.objects.filter(mentor=user.mentor, session_date__gte=now).order_by('session_date')
        completed_sessions = Booking.objects.filter(mentor=user.mentor, session_date__lt=now).order_by('-session_date')
    
    context = {
        'upcoming_sessions': upcoming_sessions,
        'completed_sessions': completed_sessions,
        'user_role': user.role
    }
    return render(request, 'booking.html', context)

@login_required
def book_session_view(request, mentor_id):
    mentor = Mentor.objects.get(pk=mentor_id)
    if request.method == 'POST':
        if request.user.role != 'learner':
            messages.error(request, "Only learners can book sessions.")
            return redirect('home')

        date_str = request.POST.get('session_date')
        time_str = request.POST.get('session_time')
        session_datetime_str = f'{date_str} {time_str}'
        session_dt_naive = datetime.strptime(session_datetime_str, '%Y-%m-%d %H:%M')
        session_dt_aware = timezone.make_aware(session_dt_naive)

        if session_dt_aware < timezone.now():
            messages.error(request, "You cannot book a session in the past.")
            return render(request, 'book_session_form.html', {'mentor': mentor})

        Booking.objects.create(learner=request.user.learner, mentor=mentor, session_date=session_dt_aware, status='confirmed')
        messages.success(request, f"Session with {mentor.user.full_name} booked successfully!")
        return redirect('booking')

    return render(request, 'book_session_form.html', {'mentor': mentor})

@login_required
def award_points_view(request, session_id):
    if request.method == 'POST':
        session = Booking.objects.get(id=session_id, learner=request.user.learner)
        points = int(request.POST.get('points'))
        session.points_awarded = points
        session.save()
        
        mentor = session.mentor
        mentor.points += points
        mentor.save()
        
        return redirect('booking')
    return redirect('booking')

@login_required
def mentor_profiles_view(request):
    mentors = Mentor.objects.all().order_by('-points')
    return render(request, 'mentor_profiles.html', {'mentors': mentors})

@login_required
def leaderboard_view(request):
    ranked_mentors = Mentor.objects.all().order_by('-points')[:10]
    return render(request, 'leaderboard.html', {'mentors': ranked_mentors})

@login_required
def progress_tracker_view(request):
    learner = request.user.learner
    completed_sessions = Booking.objects.filter(learner=learner, session_date__lt=timezone.now()).order_by('-session_date')
    context = {
        'completed_sessions': completed_sessions,
        'session_count': completed_sessions.count(),
        'total_points': completed_sessions.aggregate(total=Sum('points_awarded'))['total'] or 0,
    }
    return render(request, 'progress_track.html', context)

@login_required
def diet_plans_view(request):
    learner = request.user.learner
    matching_plans = DietPlan.objects.filter(goal=learner.goal)
    context = {
        'diet_plans': matching_plans,
        'learner_goal': learner.get_goal_display()
    }
    return render(request, 'diet_plans.html', context)