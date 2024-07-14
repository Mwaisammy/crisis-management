from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default='Bio information not provided')
    location = models.CharField(max_length=200)
    email = models.EmailField(default='example@example.com')
    phone_number = models.CharField(default='123-456-7890', max_length=20)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')



    def __str__(self):
        return self.user.username 


class Alert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)   
    title = models.CharField(max_length=250)
    description = models.TextField()
    location = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    visibility = models.CharField(max_length=20, choices=[('public', 'Public'), ('private', 'Private')], default='public')


    def __str__(self):
        return self.title 


class Resource(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    available = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.name
    

class EmergencyContact(models.Model):
    name = models.CharField(max_length=250)
    phone = models.CharField(max_length=20)
    email = models.EmailField(default='contact@example.com')
    organization = models.CharField(max_length=250)


    def __str__(self):
        return f"{self.name} ({self.organization})"

class ResourceRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Resource_type = models.CharField(max_length=100)
    description = models.TextField()
    date_requested = models.DateTimeField(auto_now_add=True)
    is_fulfilled = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.user.username} - {self.Resource_type}"
    

class ForumPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title 


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=250,  default='')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"   
