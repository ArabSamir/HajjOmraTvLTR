from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from Accounts.models import User
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Training(models.Model):

	STATUS = (
		(0,"مسودة"),
		(1,"ينشر")
	)

	title = models.CharField(verbose_name=_('عنوان الدورة'),max_length=250 )
	content = RichTextUploadingField(verbose_name=_('المحتوى'),)
	image = models.ImageField(verbose_name=_('الصورة'),null=True)
	description = models.TextField(verbose_name=_('الوصف'),max_length=250 , blank=True,null=True)
	price = models.DecimalField(verbose_name=_('الثمن'),default=0,max_digits=7, decimal_places=2)
	price_dzd = models.DecimalField(verbose_name=_('الثمن'),default=0,max_digits=7, decimal_places=2)
	nb_purchase = models.IntegerField(verbose_name=_('عدد المشتريات'),default=0)
	created_on = models.DateTimeField(auto_now_add=True , null=True)
	statut = models.IntegerField(verbose_name=_('الحالة'),choices=STATUS, default=1)


	class Meta:
		ordering = ['-created_on']
		verbose_name = _('دورة')
		verbose_name_plural = _('الدورات')


	def __str__(self):
		return	self.title


class Section(models.Model):
	title = models.CharField(verbose_name=_('عنوان الوحدة'),max_length=250 )
	# description = models.TextField(verbose_name=_('الوصف'),max_length=250 , blank=True,null=True)
	content = RichTextUploadingField(verbose_name=_('المحتوى'),)
	training = models.ForeignKey(Training , verbose_name=_('الدورة'),on_delete=models.CASCADE )
	order = models.IntegerField(verbose_name=_('ترتيب الوحدة'),default=0)

	class Meta:
		ordering = ['order']
		verbose_name = _('الوحدة')
		verbose_name_plural = _('الوحدات')

	def __str__(self):
		return	self.title

class Course(models.Model):
	title = models.CharField(verbose_name=_('عنوان الدرس'),max_length=250 , blank=True,null=True)
	description =  models.TextField(verbose_name=_('الوصف'),max_length=250 , blank=True,null=True)
	content = RichTextUploadingField(verbose_name=_('المحتوى'),)
	section = models.ForeignKey(Section , verbose_name=_('الوحدة') ,on_delete=models.CASCADE )
	order = models.IntegerField(verbose_name=_('ترتيب الدرس'),default=0)
	opened = models.BooleanField(verbose_name=_('درس مفتوح'),default=False)

	class Meta:
		ordering = ['order']
		verbose_name = _('الدرس')
		verbose_name_plural = _('الدروس')

	def __str__(self):
		return	self.title
class UserTraining(models.Model):
	user = models.ForeignKey(User , on_delete=models.CASCADE,verbose_name=_('المستخدم'),blank=False,null=False)
	training = models.ForeignKey(Training , on_delete=models.CASCADE,verbose_name=_('الدورة'),blank=False,null=False)
	active = models.BooleanField(verbose_name=_('فعال'),default=False)
	purchase_date = models.DateField(verbose_name=_('تاريخ الشراء'),auto_now_add=True)
  
	class Meta:
		unique_together = (("user", "training"),)
		verbose_name = _('الطلب')
		verbose_name_plural = _('الطلبات')
	
	def __str__(self):
		return	f'{self.training.title} {self.user.get_full_name()}'