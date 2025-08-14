from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('signup/', views.sign_up_selection_view, name='sign'),
    path('signup/learner/', views.learner_signup_view, name='lsignup'),
    path('signup/mentor/', views.mentor_signup_view, name='msign'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/learner/', views.learner_dashboard_view, name='learner_dash'),
    path('dashboard/mentor/', views.mentor_dashboard_view, name='mentor_dash'),
    path('mentors/', views.mentor_profiles_view, name='mentor_profiles'),
    path('bookings/', views.booking_view, name='booking'),
    path('book/<int:mentor_id>/', views.book_session_view, name='book_session'),
    path('award-points/<int:session_id>/', views.award_points_view, name='award_points'),
    path('leaderboard/', views.leaderboard_view, name='leaderboard'),
    path('progress/', views.progress_tracker_view, name='progress_tracker'),
    path('diet-plans/', views.diet_plans_view, name='diet_plans'),
]