from django.contrib import admin

# Register your models here.
from network.models import Post, Follow

admin.site.register(Post)
admin.site.register(Follow)
