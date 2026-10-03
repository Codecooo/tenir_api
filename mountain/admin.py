from django.contrib import admin

from mountain.models import Mountain, MountainPicture

# Register your models here.
admin.site.register([MountainPicture, Mountain])