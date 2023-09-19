from django.contrib import admin
from .models import Category, Post

admin.site.register(Category)

class PostAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('path/to/admin.css',),
        }
        
admin.site.register(Post, PostAdmin)
