from Training.models import Course, Section
from django import template

register = template.Library()

@register.filter
def next( course_id):
	course = Course.objects.get(id=course_id)
	section = course.section
	next_course = Course.objects.filter(section = section ,order__gt=course.order).order_by('order').first()
	if next_course:
		return next_course.id
	else:
		next_section = Section.objects.filter(training=section.training , order__gt=section.order).first()
		print(next_section)
		if next_section:
			course = Course.objects.filter(section = next_section ).order_by('order').first()
			if course:
		
				return course.id 
			else:
				return ''
		else:
			return ''

@register.filter
def next_title(course_id):
	return  Course.objects.get(id=course_id).title

@register.filter
def previous( course_id):
	course = Course.objects.get(id=course_id)
	section = course.section
	previous_course = Course.objects.filter(section = section ,order__lt=course.order).order_by('-order').first()
	if previous_course:
		return previous_course.id
	else:
		previous_section = Section.objects.filter(training=section.training , order__lt=section.order).first()
		if previous_section:
			
			course = Course.objects.filter(section = previous_section ).order_by('-order').first()
			if course:
				return course.id

			else:
				return ''
		else:
			return ''

@register.filter
def previous_title(course_id):
	return  Course.objects.get(id=course_id).title

