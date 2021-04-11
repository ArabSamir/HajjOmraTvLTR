from django.db import models
from Accounts.models import User
from django.db.models.signals import post_save , pre_save ,post_delete
from random import choice
from string import ascii_letters
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.translation import gettext_lazy as _
# seed random number generator

# Create your models here.

STATUS = (
	(0,"مسودة"),
	(1,"ينشر")
)


class Category(models.Model):
	category_name = models.CharField(verbose_name=_('إسم الفئة'),max_length=250 , blank=False , null=False)
	nb_posts = models.IntegerField(verbose_name=_('عدد المقالات'), default=0)

	@property
	def nb_posts_(pk):
		cat = Category.objects.filter(pk=pk)
		return cat.count()
	class Meta:
		verbose_name = _('ﺔﺌﻔﻟا')
		verbose_name_plural = _('الفئات')
	def __str__(self):
		return self.category_name


class Post(models.Model):
	title = models.CharField(verbose_name=_('العنواة'),max_length=250 , blank=False, null=False)
	image = models.ImageField(verbose_name=_('الصورة'),upload_to='blog/posts' ,  blank=True, null=True)
	author = models.ForeignKey(User , on_delete=models.CASCADE , blank=False , null=False,verbose_name=_('الكاتب'))
	description =  models.TextField(verbose_name=_('الشرح'),)
	content =  RichTextUploadingField(verbose_name=_('المحتوى'),)
	statut = models.IntegerField(verbose_name=_('الحالة'),choices=STATUS, default=0)
	updated_on = models.DateTimeField(auto_now= True)
	category = models.ForeignKey(Category , on_delete=models.CASCADE , blank=False , null=False,verbose_name=_('الفئة'))
	created_on = models.DateTimeField(verbose_name=_('تاريخ الإنشاء'),auto_now_add=True)
	nb_comments = models.IntegerField(verbose_name=_('عدد التعليقات'), default=0)
	
	class Meta:
		ordering = ['-created_on']
		verbose_name = _('مقال')
		verbose_name_plural = _('مقالات')

	def __str__(self):
		return self.title



class Comment(models.Model):
	post = models.ForeignKey(Post , on_delete=models.CASCADE , blank=False , null=False,verbose_name=_('المقال'))
	creator = models.ForeignKey(User , on_delete=models.CASCADE , blank=False , null=False,verbose_name=_('المعلق'))
	text = models.TextField(verbose_name=_('تعلسق'))
	created_on = models.DateTimeField(verbose_name=_('تاريخ الإنشاء'),auto_now_add=True)
	
	class Meta:
		ordering = ['-created_on']
		verbose_name = _('التعليق')
		verbose_name_plural = _('التعليقات')
		
		
	def __str__(self):
		return self.text

def update_comments_nb_more(sender , instance , **kwargs):
	if 'created' in kwargs:
		post = instance.post
		post.nb_comments += 1
		post.save()

post_save.connect(update_comments_nb_more , sender=Comment)

def update_comments_nb_less(sender , instance , **kwargs):
	post = instance.post
	post.nb_comments -= 1
	post.save()
post_delete.connect(update_comments_nb_less , sender=Comment)

def update_posts_nb_more(sender , instance , **kwargs):
	if 'created' in kwargs:
		category = instance.category
		category.nb_posts += 1
		category.save()

post_save.connect(update_posts_nb_more , sender=Post)

def update_posts_nb_less(sender , instance , **kwargs):
	category = instance.category
	category.nb_posts -= 1
	category.save()
post_delete.connect(update_posts_nb_less , sender=Post)
