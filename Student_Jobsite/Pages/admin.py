 # admin.py

from django.contrib import admin
from .models import PayRequest

@admin.register(PayRequest)
class PayRequestAdmin(admin.ModelAdmin):
    list_display = (
        'job_title',
        'job_amount',
        'requester_username',
        'requester_phone',
        'employer_username',
        'status',
        'created_at'
    )
    list_filter = ('status', 'created_at')
    search_fields = ('job_application__job__title', 'requester__username', 'job_application__job__employer__username')

    def job_title(self, obj):
        return obj.job_application.job.title

    def job_amount(self, obj):
        return f"KES {obj.job_application.job.amount}"

    def requester_username(self, obj):
        return obj.requester.username

    def requester_phone(self, obj):
        return obj.requester.phone_number

    def employer_username(self, obj):
        return obj.job_application.job.employer.username

    job_title.short_description = 'Job Title'
    job_amount.short_description = 'Amount'
    requester_username.short_description = 'Job Seeker'
    requester_phone.short_description = 'Phone Number'
    employer_username.short_description = 'Employer'
