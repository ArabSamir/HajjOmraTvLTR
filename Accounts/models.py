from django.db import models
from django.contrib.auth.models import PermissionsMixin

from django.contrib.auth.models import (
	BaseUserManager, AbstractBaseUser
)
from ckeditor.fields import RichTextField

from django.db.models.signals import post_save , pre_save
from django.utils.translation import gettext_lazy as _

import os
# Create your tests here.

class UserManager(BaseUserManager ):
	def create_user(self , email , password = None , is_staff = False , is_admin=False , is_active = True):
		if not email:
			raise ValueError('user must have an email adresse')
		user_obj = self.model(
			email = self.normalize_email(email),
					)
		user_obj.set_password(password)
		user_obj.is_staff = is_staff
		user_obj.is_admin = is_admin
		user_obj.is_active = is_active
		user_obj.save(using = self._db)
		return user_obj

	def create_staffuser(self , email  , password=None):
		user = self.create_user(
			email ,
			
			password,
			is_staff=True,
			is_active = True
			)
		return user

	def create_superuser(self , email , password=None):
		user = self.create_user(
			email ,
			password,
			is_staff=True,
			is_admin =True,
			is_active = True
			)
		return user






class User(AbstractBaseUser ,PermissionsMixin):
	email = models.EmailField(
		verbose_name='اسم المستخدم',
		max_length=255,
		unique=True,

	)
	name = models.CharField(verbose_name='الإسم',max_length=100 , null=False , blank = False)
	lastname = models.CharField(verbose_name='اللقب',max_length=100 , null=False , blank = False)
	is_active = models.BooleanField(verbose_name='فعال',default=True)
	is_staff    = models.BooleanField(verbose_name='عامل',default=False) # a admin user; non super-user
	is_admin = models.BooleanField(verbose_name='مسؤول',default=False) # a superuser
	# notice the absence of a "Password field", that's built in.
	
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = [] # Email & Password are required by default.


	def get_full_name(self):
	# The user is identified by their email address
		return f'{self.name} {self.lastname}'


	def get_short_name(self):
	# The user is identified by their email address
		return self.email

	def __str__(self):
		return self.email

	def has_perm(self, perm, obj=None):
		return self.is_admin
		
	def has_perms(self, perm, obj=None):
		return self.is_admin    
			
	def has_module_perms(self, app_label):
	   return self.is_admin

	@property
	def is_superuser(self):
		"Is the user superuser?"
		return self.superuser

	class Meta:
		verbose_name = _('المستخدم')
		verbose_name_plural = _('المستخدمين')




	objects = UserManager()



class Profile(models.Model):
	user = models.OneToOneField(User , 	 on_delete=models.CASCADE,verbose_name='المستخدم')
	image = models.ImageField(verbose_name='الصورة',default = '../static/img/profile.png' , upload_to='profile/', blank=True , null=True)
	birth_date = models.DateTimeField( verbose_name='تاريخ الميلاد'  ,blank=True , null=True)
	gender  = models.CharField(verbose_name='الجنس'   ,max_length=250 , blank=True , null=True)

	class Meta:
		verbose_name = _('الملف الشخصي')
		verbose_name_plural = _('الملفات الشخصية')



	def __str__(self):
		return f'{self.user.name} {self.user.lastname}'


def create_user_profile(sender , instance , **kwargs):
	if kwargs['created']:
			
		profile = Profile(user=instance)
		profile.save()

post_save.connect(create_user_profile , sender=User)






class Contact(models.Model) : 
	adresse  = models.CharField(   max_length=250 , blank=True , null=True,verbose_name='العنوان')
	phone = models.CharField(   max_length=250 , blank=True , null=True ,verbose_name='الهاتف')
	first_email = models.CharField(   max_length=250 , blank=True , null=True ,verbose_name='الإيميل الأول')
	secound_email = models.CharField(   max_length=250 , blank=True , null=True ,verbose_name='الإيميل الثاني')
	facebook = models.CharField(   max_length=250 , blank=True , null=True ,verbose_name='الفيسبوك')
	instagram = models.CharField(   max_length=250 , blank=True , null=True ,verbose_name='الانستغرام')
	twitter = models.CharField(   max_length=250 , blank=True , null=True ,verbose_name='تويتر')
	youtube = models.CharField(   max_length=250 , blank=True , null=True ,verbose_name='يوتوب')

	class Meta:
		verbose_name = _('التواصل')
		verbose_name_plural = _('إعدادات معلومات الاتصال')
	
	def __str__(self):
		return "الإعدادات"


class Content(models.Model):
	header_title = models.CharField(   max_length=250 , blank=True , null=True ,verbose_name='عنوان رأس الصفحة')
	header_description = models.TextField(   max_length=250 , blank=True , null=True ,verbose_name='وصف رأس الصفحة')
	website_description = models.TextField(   max_length=250 , blank=True , null=True ,verbose_name='وصف الموقع ')
	logo = models.ImageField(upload_to='images/' ,  default='../static/img/photo1.jpg',verbose_name='صورة الشعار')
	logo_white = models.ImageField(upload_to='images/' ,  default='../static/img/photo1.jpg',verbose_name='صورة الشعار الأبيض')
	favicon = models.ImageField(upload_to='images/' ,  default='../static/img/photo1.jpg',verbose_name='صورة أيقونة الشعار')
	og_image = models.ImageField(upload_to='images/' ,  default='../static/img/photo1.jpg',verbose_name='صورة الوصف' )
	header_image = models.ImageField(upload_to='images/' ,  default='../static/img/photo1.jpg',verbose_name='صورة رأص الصفحة')
	
	about_us_title = models.CharField(   max_length=250 , blank=True , null=True ,verbose_name='عنوان صفحة من نحن')
	about_us_description = RichTextField(  verbose_name='وصف صفحة من نحن' )
	about_us_image = models.ImageField(upload_to='images/' ,  default='../static/img/photo1.jpg',verbose_name='صورة صفحة من نحن')
	
	videos_title = models.CharField(   max_length=250 , blank=True , null=True ,verbose_name='عنوان قسم الفيديوهات')
	subscribe_text = models.TextField(   max_length=250 , blank=True , null=True ,verbose_name='محتوى إشترك معنا')
	subscribe_url = models.CharField(   max_length=250 , blank=True , null=True ,verbose_name='رابط إشترك معنا')
	
	blog_title = models.CharField(   max_length=250 , blank=True , null=True ,verbose_name='عنوان قسم المقالات')
	
	header_title_s = models.CharField(   max_length=250 , blank=True , null=True ,verbose_name='عنوان رأس الصفحة الثاني')
	header_description_s = models.TextField(   max_length=250 , blank=True , null=True ,verbose_name='وصف رأس الصفحة الثاني')
	header_image_s = models.ImageField(upload_to='images/' ,  default='../static/img/photo1.jpg',verbose_name='صورة رأ الثانيةص الصفحة' )
	
	paypal_client_id = models.CharField(   max_length=250 , blank=True , null=True ,verbose_name='رقم عميل PayPal')
	ccp = models.CharField(   max_length=250 , blank=True , null=True ,verbose_name='رقم  الحساب')
	class Meta:
		verbose_name = _('المحتوى')
		verbose_name_plural = _('إعدادات المتحويات')

	def __str__(self):
		return "الإعدادات"


class Video (models.Model):
	title = models.CharField(   max_length=250 , blank=True , null=True ,verbose_name='العنوان')
	description = models.CharField(   max_length=250 , blank=True , null=True,verbose_name='الوصف')
	url = models.CharField(   max_length=250 , blank=True , null=True,verbose_name='عنوان URL')
	image = models.ImageField(upload_to='videos/' ,  default='../static/img/photo1.jpg',verbose_name='الصورة')



	class Meta:
		verbose_name = _('فيديو')
		verbose_name_plural = _('الفيديوهات')


	def __str__(self):
		return self.title
