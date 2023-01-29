from django.contrib import admin
from django.urls import path, include
from blogApp import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

admin.site.site_header = "Admin"
admin.site.site_title = "Coder's Blog Admin Panel"
admin.site.index_title = "Welcome to Coder's Blog Admin Panel"


urlpatterns = [
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('abdullah_admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    path('', views.index, name='index'),
    path('account_details', views.account_details, name='account_details'),
    path('blog/<int:id>', views.content, name='blog_content'),
    path('search', views.search, name='search_results'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('courses', views.courses, name='courses'),
    path('course/<int:id>', views.course_info, name='course_info'),
    path('buy_course/<int:id>', views.buy_course, name='buy_course'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('edit_course/<int:id>', views.edit_course, name='edit_course'),
    path('delete_course/<int:id>', views.delete_course, name='delete_course'),
    path('download_file/<slug:sessionId>', views.download_file, name='download_file'),
    path('purchased_courses', views.purchased_courses, name='purchased_courses'),
    path('upload_blog', views.upload_blog, name='upload_blog'),
    path('edit_blog/<int:id>', views.edit_blog, name='edit_blog'),
    path('delete_blog/<int:id>', views.delete_blog, name='delete_blog'),
    path('upload_course', views.upload_course, name='upload_course'),
    path('signup', views.signup, name='signup'),
    path('stripe_connect', views.stripe_connect, name='stripe_connect'),
    path('settings', views.setting, name='settings'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),

    path('reset_password', auth_views.PasswordResetView.as_view(), name="reset_password"),
    path('password_reset_sent', auth_views.PasswordResetDoneView.as_view(), name="reset_password_sent"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('password_reset_complete', auth_views.PasswordResetCompleteView.as_view(template_name= 'blog/password_reset_complete_page.html'), name="password_reset_complete"),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
