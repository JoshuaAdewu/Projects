from django.contrib import admin
from .models import User,Report, Ban, Node
# Register your models here.
admin.site.register(Node)
admin.site.register(Report)
admin.site.register(User)
admin.site.register(Ban)