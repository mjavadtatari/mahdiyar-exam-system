from django.contrib import admin
from jalali_date.admin import ModelAdminJalaliMixin, StackedInlineJalaliMixin, TabularInlineJalaliMixin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from .models import *

admin.site.register(User, UserAdmin)
admin.site.register(Klass)
admin.site.register(Academy)
admin.site.register(StudentScore)
admin.site.register(Notification)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Exam)
admin.site.register(Category)
admin.site.register(ExamPerStudent)
admin.site.register(Wallet)
admin.site.register(Transaction)
admin.site.register(SignUpKey)


@admin.register(Profile)
class ProfileAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    pass
