from django.contrib import admin
 
from .models import Post, Images
 
class ImagesAdmin(admin.StackedInline):
    model = Images
 
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [ImagesAdmin]
 
    class Meta:
       model = Post
 
@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    pass