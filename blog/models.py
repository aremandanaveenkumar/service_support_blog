from django.db import models
from django.contrib.auth.models import User
from address.models import AddressField

STATUS = ((0, "Draft"), (1, "Published"), 
          (2, "NotRectified"), (3,  "Rectified"))

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer_name")
    customer_address = models.ForeignKey(AddressField, on_delete=models.CASCADE, related_name='+')
    problem_reported = models.TextField()
    retification = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)

