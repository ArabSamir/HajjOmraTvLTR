from Blog.models import Category , Post
from django import template

register = template.Library()



@register.filter
def category_nb(category_id):
	return  Post.objects.filter(category=Category.objects.get(id=category_id)).count()