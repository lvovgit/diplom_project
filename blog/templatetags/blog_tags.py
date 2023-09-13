from django import template
from django.db.models import Count
from taggit.models import Tag

from blog.models import Category, Post

register = template.Library()


def get_all_categories():
    return Category.objects.all()

# def get_all_tags():
#     return Tag.objects.all()

# @register.simple_tag()
# def get_list_tags():
#     """Вывод списка тегов"""
#     return get_all_tags()

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


@register.simple_tag()
def get_last_post():
    last_post = Post.objects.order_by("-create_at")[0:1]

    return {
        'last_post': last_post,
    }
