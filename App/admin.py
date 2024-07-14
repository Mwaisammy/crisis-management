from django.contrib import admin
from .models import Profile, Alert, Resource, EmergencyContact, ResourceRequest, ForumPost, Comment #CustomUser

# Register your models here.
# class AlertInline(admin.TabularInline):
#     model = Alert

admin.site.register(Alert)
admin.site.register(Profile)
admin.site.register(Resource)
admin.site.register(EmergencyContact)
admin.site.register(ResourceRequest)
admin.site.register(ForumPost)
admin.site.register(Comment)
