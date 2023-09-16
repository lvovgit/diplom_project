from django import template
from django.db.models import Count
from taggit.models import Tag

from blog.models import Category

register = template.Library()


def get_all_categories():
    return Category.objects.all()


@register.simple_tag()
def popular_tags():
    """Вывод списка популярных тегов"""
    tags = Tag.objects.annotate(num_times=Count('post')).order_by('-num_times')
    tag_list = list(tags.values('name', 'num_times', 'slug'))
    return tag_list


@register.simple_tag()
def get_list_category():
    """Вывод списка категорий"""
    return get_all_categories()
