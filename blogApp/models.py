from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User



class Blog_post(models.Model):
    title = models.CharField(max_length=255)
    desc = HTMLField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title


class StripeInfo(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    stripe_account_id = models.CharField(max_length=500)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.stripe_account_id


class Course(models.Model):
    title = models.CharField(max_length=255)
    shortdesc = models.CharField(max_length=500)
    price = models.CharField(max_length=300)
    content = HTMLField()
    course_thumbnail = models.FileField(upload_to='thumbnail/')
    course_file = models.FileField(upload_to='files/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=500)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title


class PurchasedCourse(models.Model):
    # status_choices = {
    #     ('S', 'Succeeded'),
    #     ('R', 'Refunded'),
    #     ('U', 'Uncaptured'),
    #     ('F', 'Failed')
    # }
    payment_id = models.TextField()
    customer_email = models.EmailField()
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    # status = models.CharField(max_length=2, choices=status_choices)
    status = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.customer_email






















