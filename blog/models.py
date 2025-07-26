from django.db import models
from django.contrib.auth.models import User

STATUS = ((0, "Draft"), (1, "Published"), 
          (2, "NotRectified"), (3,  "Rectified"))

# Create your models here.
class AddressField(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state}, {self.country}"

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")
    customer = models.CharField(max_length=100)
    customer_address = models.ForeignKey(AddressField, on_delete=models.CASCADE, related_name='+')
    problem_reported = models.TextField()
    retification = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    excerpt = models.TextField(blank=True)

