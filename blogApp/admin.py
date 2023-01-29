from django.contrib import admin
from .models import Blog_post, Course, PurchasedCourse, StripeInfo


@admin.register(Blog_post)
class BlogModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user', 'created_at', 'updated_at']


@admin.register(Course)
class CourseModel(admin.ModelAdmin):
    list_display = ['id', 'title', 'shortdesc', 'price', 'course_file', 'user', 'content', 'created_at', 'updated_at']
    
    
@admin.register(PurchasedCourse)
class PurchasedCourseModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_email', 'username', 'course_id', 'status', 'created_at', 'updated_at']


@admin.register(StripeInfo)
class StripeInfoModel(admin.ModelAdmin):
    list_display = ['id', 'username', 'stripe_account_id', 'created_at', 'updated_at']

