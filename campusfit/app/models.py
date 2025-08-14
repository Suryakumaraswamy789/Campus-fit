from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (('learner', 'Learner'), ('mentor', 'Mentor'))
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, null=True, blank=True)
    full_name = models.CharField(max_length=100)

class Learner(models.Model):
    GOAL_CHOICES = (
        ('weight_loss', 'Weight Loss'),
        ('muscle_gain', 'Muscle Gain'),
        ('stamina', 'Stamina/Endurance'),
        ('flexibility', 'Flexibility'),
        ('sports', 'Sports Performance'),
        ('rehabilitation', 'Rehabilitation'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    roll_number = models.CharField(max_length=20, blank=True)
    goal = models.CharField(max_length=20, choices=GOAL_CHOICES)

    def __str__(self):
        return self.user.full_name

class Mentor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    specialization = models.CharField(max_length=100)
    experience = models.PositiveIntegerField()
    bio = models.TextField(max_length=250)
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.user.full_name

class Booking(models.Model):
    STATUS_CHOICES = (('confirmed', 'Confirmed'), ('completed', 'Completed'))
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE)
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    session_date = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='confirmed')
    points_awarded = models.IntegerField(default=0)

    def __str__(self):
        return f"Session with {self.mentor.user.full_name} for {self.learner.user.full_name}"

class DietPlan(models.Model):
    GOAL_CHOICES = Learner.GOAL_CHOICES
    goal = models.CharField(max_length=20, choices=GOAL_CHOICES)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    content = models.TextField()

    def __str__(self):
        return self.title