from django import template
from news.models import Category
from django.db.models import *
from django.core.cache import cache

register = template.Library()


# @register.simple_tag(name='get_list_categories')
# def get_categories():
#     # return Category.objects.all()
#     return Category.objects.annotate(cnt=Count('news')).filter(cnt__gt=0)
# <!--<div class="list-group">-->
# <!--    {% get_list_categories as categories %}-->
# <!--    {% for category in categories %}-->
# <!--    <a href="{% url 'category' category.pk %}" class="list-group-item list-group-item-action"> {{ category.title }}-->
# <!--        <span class="category-count">{{ category.cnt }}</span>-->
# <!--    </a>-->
# <!--    {% endfor %}-->
# <!--</div>-->
#

@register.inclusion_tag('news/list_categories.html')
def show_categories(arg1='Hello', arg2='World'):
    # categories = Category.objects.annotate(cnt=Count('news')).filter(cnt__gt=0)
    # categories = cache.get('categories')
    # if not categories:
    #     categories = Category.objects.annotate(cnt=Count('news', filter=F('news__is_published'))).filter(cnt__gt=0)
    #     cache.set('categories', categories, 30)
    # SAME LOGIC
    # categories = cache.get_or_set('categories', Category.objects.annotate(cnt=Count('news', filter=F('news__is_published'))).filter(cnt__gt=0), 30)
    categories = Category.objects.annotate(cnt=Count('news', filter=F('news__is_published'))).filter(cnt__gt=0)
    return {"categories": categories, "arg1": arg1, "arg2": arg2}
