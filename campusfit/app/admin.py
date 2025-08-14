from django.contrib import admin
from .models import User, Learner, Mentor, Booking, DietPlan

class MentorAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'specialization', 'experience', 'has_first_aid_certification', 'passed_safety_quiz')
    list_filter = ('status', 'has_first_aid_certification')
    search_fields = ('user__full_name', 'specialization')
    readonly_fields = ('application_text', 'form_check_video_url')

admin.site.register(User)
admin.site.register(Learner)
admin.site.register(Mentor, MentorAdmin)
admin.site.register(Booking)
admin.site.register(DietPlan)