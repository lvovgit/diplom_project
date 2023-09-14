from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from blog import models
from blog.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "author", "create_at", "id"]
    search_fields = ('name', 'description',)
    list_filter = ('create_at',)
    prepopulated_fields = {"slug": ("title",)}
    save_as = True
    save_on_top = True


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'website', 'create_at', 'id']


admin.site.register(models.Category, MPTTModelAdmin)
