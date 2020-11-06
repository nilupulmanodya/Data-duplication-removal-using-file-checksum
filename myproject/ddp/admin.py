from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(User)
admin.site.register(Files)
admin.site.register(Shared)
admin.site.register(Uploads)
admin.site.register(temUploads)