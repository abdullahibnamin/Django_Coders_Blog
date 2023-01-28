from django.shortcuts import render, HttpResponseRedirect
from .forms import SignUpForm, LoginForm, UserPasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as user_login, logout as user_logout # over write issue
from django.contrib.auth import update_session_auth_hash
from django.core.mail import send_mail
from django.conf import settings
from django.core.paginator import Paginator
from .models import Blog_post, Course, User, PurchasedCourse, StripeInfo
from django.http import FileResponse
import stripe
import logging
from math import ceil


stripe.api_key = settings.STRIPE_API_KEY
db_logger = logging.getLogger('db')


def index(request):
    allblogs = Blog_post.objects.all().order_by('-id')
    paginator = Paginator(allblogs, 3)
    page_number = request.GET.get('page')
    blogs = paginator.get_page(page_number)
    page_count = str(blogs)[1:-1]
    return render(request, 'blog/index.html', { "blogs": blogs, 'page_count': page_count })


@login_required(login_url='/login')
def account_details(request):
    if request.user.is_authenticated:
        user_obj = User.objects.get(username = request.user.username)
        context = {
            'username' : user_obj.username,
            'user_email' : user_obj.email,
            'user_firstname' : user_obj.first_name,
            'user_lastname' : user_obj.last_name,
            'user_fullname' : user_obj.get_full_name(),
            'user_isauthenticated' : user_obj.is_authenticated,
            'user_isactive' : user_obj.is_active,
            'user_lastlogin' : user_obj.last_login,
            'user_date_joined' : user_obj.date_joined
        }
        return render(request, 'blog/user_accountdetails.html', context=context)


def content(request, id):
    blog = Blog_post.objects.get(id=id)
    return render(request, 'blog/blog_content.html', {"blog": blog})


def search(request):
    query = request.GET['query']
    if len(query) > 40:
        search_result = Blog_post.objects.none()
    else:
        search_title = Blog_post.objects.filter(title__icontains=query)
        search_content = Blog_post.objects.filter(desc__icontains=query)
        search_result = search_title.union(search_content)

    return render(request, 'blog/search_result.html', {"search_results": search_result, 'query': query})


def courses(request):
    allcourses = Course.objects.all().order_by('-id')
    return render(request, 'blog/course_page.html', {'allcourses': allcourses})


def course_info(request, id):
    coursedetail = Course.objects.get(id=id)
    return render(request, 'blog/course_info.html', {'coursedetail': coursedetail})


@login_required(login_url='/login')
def delete_course(request, id):
    course = Course.objects.get(id = id)
    course.delete()
    messages.success(request, 'Course Deleted Successfully')
    return HttpResponseRedirect('/upload_course')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Registration Done!')
            form.save()
        else:
            messages.warning(request, 'Something went wrong !!')
            return HttpResponseRedirect('/signup')
    else:
        form = SignUpForm()
    return render(request, 'blog/signup.html', {'form': form})


def login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                user_name = form.cleaned_data['username']
                user_pass = form.cleaned_data['password']
                user = authenticate(username=user_name, password=user_pass)
                print("hhhhe")
                if user is not None:
                    user_login(request, user)
                    messages.success(request, 'Logged in successfully !!')
                    return HttpResponseRedirect('/upload_blog')
            else:
                messages.warning(request, 'Something went wrong !!')
                return HttpResponseRedirect('/login') 
        else:
            form = LoginForm()
            return render(request, 'blog/login.html', {'form': form})
    else:
        return HttpResponseRedirect('/upload_blog')


@login_required(login_url='/login')
def setting(request):
    if request.user.is_authenticated:
        try:
            is_stripe_connected = bool(StripeInfo.objects.get(username = request.user))
        except StripeInfo.DoesNotExist:
            is_stripe_connected = False
        
        if request.method == 'POST':
            form = UserPasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Your Password has been changed")
                return HttpResponseRedirect('/upload_blog')
            else:
                messages.warning(request, "Error")
                return HttpResponseRedirect('/settings')
        else:
            form = UserPasswordChangeForm(request.user, request.POST)
            return render(request, "blog/setting_page.html", {'form':form, "is_stripe_connected": is_stripe_connected})


@login_required(login_url='/login')
def upload_blog(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            userBlogTitle = request.POST['blogTitle']
            userBlogDesc = request.POST['blogDesc']
            saveBlog = Blog_post(title=userBlogTitle, desc=userBlogDesc, user=user)
            saveBlog.save()
            return HttpResponseRedirect('/')
        
        allUserBlogs = Blog_post.objects.filter(user = user).order_by('-id')
        paginator = Paginator(allUserBlogs, 5)
        page_number = request.GET.get('page')
        userBlogs = paginator.get_page(page_number)
        page_count = str(userBlogs)[1:-1]

        return render(request, 'blog/add_blog.html', context={'userBlogs': userBlogs, 'page_count': page_count})


@login_required(login_url='/login')
def edit_blog(request, id):
    if request.user.is_authenticated:
        userBlog = Blog_post.objects.get(id=id)
        if request.method == "POST":
            try:
                edited_blog_title = request.POST['editedBlogTitle']
                edited_blog_desc = request.POST['editedBlogDesc']
                userBlog.title = edited_blog_title
                userBlog.desc = edited_blog_desc
                userBlog.save()
                messages.success(request, 'Successfully Blog Updated')
                return HttpResponseRedirect('/upload_blog')
            except Exception as e:
                messages.warning(request, 'Failed to update blog')
                return HttpResponseRedirect('/upload_blog')

        return render(request, 'blog/blog_edit_page.html', context={'userBlog': userBlog})


@login_required(login_url='/login')
def delete_blog(request, id):
    blog_post = Blog_post.objects.get(id=id)
    blog_post.delete()
    messages.success(request, 'Blog Deleted Successfully')
    return HttpResponseRedirect('/upload_blog')


@login_required(login_url='/login')
def upload_course(request):
    if request.user.is_authenticated:
        user = request.user
        
        try:
            s_id = StripeInfo.objects.get(username = user)
        except StripeInfo.DoesNotExist:
            s_id = None
        
        if request.method == 'POST':
            course_title = request.POST['courseTitle']
            course_short_desc = request.POST['courseShortDesc']
            
            str_course_price = request.POST['coursePrice']
            course_price_calcu = int(str_course_price) + (int(str_course_price) * (25/100))
            final_course_price = str(course_price_calcu)

            course_zip_file = request.FILES['courseZipFile']
            course_thumbnail_img = request.FILES['courseImg']
            course_desc = request.POST['courseDesc']

            course = Course(title = course_title,
                shortdesc = course_short_desc, price = final_course_price,
                content = course_desc,
                course_file = course_zip_file,
                course_thumbnail = course_thumbnail_img,
                user = user,
                stripe_id = s_id.stripe_account_id
            )
            
            course.save()
            messages.success(request, 'Course Uploaded Successfully')
            return HttpResponseRedirect('/upload_course')
        
        allUserCourses = Course.objects.filter(user = user).order_by('-id')
        paginator = Paginator(allUserCourses, 5)
        page_number = request.GET.get('page')
        user_courses = paginator.get_page(page_number)
        page_count = str(user_courses)[1:-1]
        
        return render(request, 'blog/add_course.html', {'user_courses': user_courses, 'page_count': page_count, 's_id': bool(s_id)})


@login_required(login_url='/login')
def edit_course(request, id):
    if request.user.is_authenticated:
        course = Course.objects.get(id=id)
        if request.method == 'POST':
            try:
                edited_course_title = request.POST['editedCourseTitle']
                edited_course_short_desc = request.POST['editedCourseShortDesc']
                edited_course_thumbnail = request.FILES['editedCourseThumbnail']
                edited_course_zipFile = request.FILES['editedCourseZipFile']
                edited_course_content = request.POST['editedCourseContent']

                str_edited_course_price = request.POST['editedCoursePrice']
                course_price_calcu = int(str_edited_course_price) + (int(str_edited_course_price) * (20/100))
                final_course_price = str(course_price_calcu)

                course.title = edited_course_title
                course.shortdesc = edited_course_short_desc
                course.course_thumbnail = edited_course_thumbnail
                course.price = final_course_price
                course.course_file = edited_course_zipFile
                course.content = edited_course_content
                course.save()

                messages.success(request, 'Successfully Course Updated')
                return HttpResponseRedirect('/upload_course')
            
            except Exception as e:
                messages.warning(request, 'Failed to Update Course')
                return HttpResponseRedirect('/upload_course')
        return render(request, 'blog/course_edit.html', {'course': course})


@login_required(login_url='/')
def stripe_connect(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            try:
                stripe_id = stripe.Account.create(
                    type ="custom",
                    email = request.user.email,
                    capabilities = {
                        "card_payments": {"requested": True},
                        "transfers": {"requested": True},
                    },
                    business_type = "individual"
                )

                stripe_account_info = StripeInfo(
                    username = request.user,
                    stripe_account_id = stripe_id['id']
                )

                stripe_account_info.save()

                link = stripe.AccountLink.create(
                    account = stripe_id['id'],
                    refresh_url = "http://localhost:8000/",
                    return_url = f"{request.headers['Origin']}/settings",
                    type = "account_onboarding",
                    collect = "currently_due"
                )
                return HttpResponseRedirect(link['url'])

            except Exception as e:
                db_logger.error(e)


@login_required(login_url='/login')
def buy_course(request, id):
    if request.user.is_authenticated:
        course = Course.objects.get(id=id)
        if request.method == 'POST':
            session = stripe.checkout.Session.create(
            line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': course.title,
                },
                'unit_amount': ceil(float(course.price)) * 100,
            },
            'quantity': 1,
            }],
            customer_email = User.objects.get(username=request.user).email,
            client_reference_id = course.id,
            metadata = {'customer_username': request.user},
            payment_intent_data = {
                'application_fee_amount': ceil(float((course.price)) * (25/100)) *100,
                'transfer_data': {
                    'destination': course.stripe_id
                }
            },
            mode='payment',
            success_url=f"{request.headers['Origin']}/payment_success?session_id="+"{CHECKOUT_SESSION_ID}",
            cancel_url= f"{request.headers['Origin']}/courses",
        )
    return HttpResponseRedirect(session.url)


@login_required(login_url='/login')
def payment_success(request):
    if request.user.is_authenticated:
        session = stripe.checkout.Session.retrieve(request.GET['session_id'])
        course = Course.objects.get(id=session.client_reference_id)

        if request.user.username == session.metadata['customer_username']:
            purchased_course = PurchasedCourse(
                payment_id = session.id,
                customer_email = session.customer_email,
                username = request.user,
                course_id = course,
                status = session.status
            )
        
        purchased_course.save()
        
        context = {
            'payment_id': session.id,
            'email': session.customer_email,
            'username': session.metadata['customer_username'],
            'course_title': course.title,
            'amount': session.amount_total,
            'status': session.status,
            'client_reference_id': session.client_reference_id,
            'datetime': PurchasedCourse.objects.get(payment_id=session.id).updated_at
        }

        return render(request, 'blog/payment_success_page.html', context=context)


@login_required(login_url='/login')
def download_file(request, sessionId):
    if request.user.is_authenticated:
        if request.method == 'POST':
            ssid = stripe.checkout.Session.retrieve(sessionId)
            payment_id = request.POST['pid']
            payment_username = request.POST['uname']
            payment_client_reference_id = request.POST['cid']
            payment_status = request.POST['status']

            if (ssid.id == payment_id and 
                ssid.client_reference_id == payment_client_reference_id and
                ssid.metadata['customer_username'] == payment_username and
                ssid.status == payment_status):

                course_obj = Course.objects.get(id=ssid.client_reference_id)
                filename = course_obj.course_file.path
                response = FileResponse(open(filename, 'rb'))
                
                return response


@login_required(login_url='/login')
def purchased_courses(request):
    if request.user.is_authenticated:
        purchased_courses_obj = PurchasedCourse.objects.select_related().filter(username = request.user)
        # print(courses_obj[0].course_id.price)
        return render(request, 'blog/purchased_courses_pages.html', {'purchasedCourseObj': purchased_courses_obj})


def about(request):
    return render(request, 'blog/about.html')


def contact(request):
    if request.method == 'POST':
        from_email = request.POST['contactFormEmail']
        contact_form_message = request.POST['contactFormMsg']
        try:
            send_mail(
                "Coder's Blog Contact Form",
                f'{contact_form_message}',
                f'{from_email}',
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
            messages.success(request, "Thank You")
            return HttpResponseRedirect('/contact')
        except Exception as e:
            messages.warning(request, "Error")
            return HttpResponseRedirect('/contact')
    return render(request, 'blog/contact.html')



def logout(request):
    user_logout(request)
    return HttpResponseRedirect('/')








































