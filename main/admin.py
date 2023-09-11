from django.contrib import admin

from main.models import Feedback


# Register your models here.


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    """
    Админ-панель модели профиля
    """
    list_display = ('email', 'user')
    list_display_links = ('email', )

