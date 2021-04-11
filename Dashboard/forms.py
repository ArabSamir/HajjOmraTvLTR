from Training.models import *
from Blog.models import *
from Accounts.models import *
from django import forms

STATUS = (
	(0,"مسودة"),
	(1,"ينشر")
	)

class TrainingForm(forms.ModelForm):
	training_id = None
	title = forms.CharField(label= 'العنوان' ,widget=forms.TextInput(attrs={'class': 'form-control'}), required = True)
	price = forms.CharField(label= 'السعر باليورو ' ,widget=forms.TextInput(attrs={'class': 'form-control'}), required = True)	
	price_dzd = forms.CharField(label= 'السعر  بالدينار ' ,widget=forms.TextInput(attrs={'class': 'form-control'}), required = True)	
	description = forms.CharField(label= 'الوصف' ,widget=forms.Textarea(attrs={'class': 'form-control'}), required = True)	
	statut = forms.CharField(label='الحالة',widget=forms.Select(attrs={'class': 'form-control '  } ,choices=STATUS ),required = False)
	
	class Meta:
		model = Training
		fields = (
				'title',
				'description',
				'price',
				'price_dzd',
				'content',
				'image',
				'statut',
			)

class SectionForm(forms.ModelForm):
	def __init__(self,*args,**kwargs):
		self.training_id =  kwargs.pop('training_id')
		super(SectionForm,self).__init__(*args,**kwargs)
		choices = ()
		index = 1
		sections = Section.objects.filter(training=Training.objects.get(pk=self.training_id))
		if sections:

			for  section  in sections:
				choices = choices + ((index , index),)
				index += 1
				
				if index == len(sections)+1:
					choices = choices + ((index , index),)
		else:
			choices = choices + ((1 , 1),)

		self.fields['order'].choices = choices
	
	try:
		choices=[ (choice.order, choice.order) for choice in Section.objects.all()]
		
	except Exception as e:
		choices = ()
	title = forms.CharField(label= 'العنوان' ,widget=forms.TextInput(attrs={'class': 'form-control'}), required = True)
	order = forms.ChoiceField(label= 'الترتيب' ,choices=choices,widget=forms.Select(attrs={'class': 'form-control', }), required = True)	

	class Meta:
		model = Section
		fields = (
				'title',
				'order',
			)

class CourseForm(forms.ModelForm):
	def __init__(self,*args,**kwargs):
		self.section_id =  kwargs.pop('section_id')
		super(CourseForm,self).__init__(*args,**kwargs)
		choices = ()
		index = 1
		courses = Course.objects.filter(section=Section.objects.get(pk=self.section_id))
		if courses:
			for  course  in courses:
				choices = choices + ((index , index),)
				index += 1
				
				if index == len(courses)+1:
					choices = choices + ((index , index),)
		else:
			choices = ((1 , 1),)
		self.fields['order'].choices = choices
	
	title = forms.CharField(label= 'العنوان' ,widget=forms.TextInput(attrs={'class': 'form-control'}), required = True)
	order = forms.ChoiceField(label= 'الترتيب' ,widget=forms.Select(attrs={'class': 'form-control','type': 'number', }), required = True)	

	class Meta:
		model = Course
		fields = (
				'title',
				'order',
				'content',
				'opened',
			)



class PostForm(forms.ModelForm):
	
	title = forms.CharField(label= 'العنوان' ,widget=forms.TextInput(attrs={'class': 'form-control'}), required = True)
	description = forms.CharField(label= 'الوصف' ,widget=forms.Textarea(attrs={'class': 'form-control'}), required = True)	
	statut = forms.CharField(label='الحالة',widget=forms.Select(attrs={'class': 'form-control '  } ,choices=STATUS ),required = False)
	category = forms.ModelChoiceField(label='الفئة',widget=forms.Select(attrs={  'class':'form-control'}),queryset = Category.objects.all())
	
	class Meta:
		model = Post
		fields = (
				'title',
				'description',
				'category',
				'statut',
				'image',
				'content',
			)




class CategoryForm(forms.ModelForm):

	category_name = forms.CharField(label= 'اسم الفئة' ,widget=forms.TextInput(attrs={'class': 'form-control'}), required = True)

	class Meta:
		model = Category
		fields = (
				'category_name',
			)



class ContentForm(forms.ModelForm):

	header_title =forms.CharField(label= 'عنوان رأس الصفحة',widget=forms.TextInput(attrs={'class': 'form-control'}), required = False)
	header_description = forms.CharField(label= 'وصف رأس الصفحة' ,widget=forms.Textarea(attrs={'class': 'form-control'}), required = False)
	about_us_title = forms.CharField(label= 'عنوان صفحة من نحن',widget=forms.TextInput(attrs={'class': 'form-control'}), required = False)
	videos_title =forms.CharField(label= 'عنوان قسم الفيديوهات',widget=forms.TextInput(attrs={'class': 'form-control'}), required = False)
	blog_title = forms.CharField(label= 'عنوان قسم المقالات',widget=forms.TextInput(attrs={'class': 'form-control'}), required = False)

	header_title_s = forms.CharField(label= 'عنوان رأس الصفحة الثاني',widget=forms.TextInput(attrs={'class': 'form-control'}), required = False)
	header_description_s = forms.CharField(label= 'وصف رأس الصفحة الثاني',widget=forms.Textarea(attrs={'class': 'form-control'}), required = False)

	website_description = forms.CharField(label= 'وصف الموقع ' ,widget=forms.Textarea(attrs={'class': 'form-control'}), required = False)
	subscribe_text = forms.CharField(label= 'محتوى إشترك معنا' ,widget=forms.Textarea(attrs={'class': 'form-control'}), required = False)
	subscribe_url = forms.CharField(label= 'رابط إشترك معنا',widget=forms.TextInput(attrs={'class': 'form-control'}), required = False)

	paypal_client_id = forms.CharField(label= 'رقم عميل PayPal',widget=forms.TextInput(attrs={'class': 'form-control'}), required = False)
	ccp = forms.CharField(label= 'رقم  حساب  CCP',widget=forms.TextInput(attrs={'class': 'form-control'}), required = False)

	class Meta:
		model = Content
		fields = '__all__'





class ContactForm(forms.ModelForm):
	adresse  = forms.CharField(label= 'العنوان',widget=forms.TextInput(attrs={'class': 'form-control'}), required = True)
	phone = forms.CharField(label= 'الهاتف',widget=forms.TextInput(attrs={'class': 'form-control'}), required = True)
	first_email = forms.CharField(label= 'الإيميل الأول',widget=forms.TextInput(attrs={'class': 'form-control'}), required = True)
	secound_email = forms.CharField(label='الإيميل الثاني',widget=forms.TextInput(attrs={'class': 'form-control'}), required = True)
	facebook = forms.CharField(label= 'الفيسبوك',widget=forms.TextInput(attrs={'class': 'form-control'}), required = True)
	instagram = forms.CharField(label= 'الانستغرام',widget=forms.TextInput(attrs={'class': 'form-control'}), required = True)
	twitter = forms.CharField(label= 'تويتر',widget=forms.TextInput(attrs={'class': 'form-control'}), required = True)
	youtube = forms.CharField(label= 'يوتوب',widget=forms.TextInput(attrs={'class': 'form-control'}), required = True)

	class Meta:
		model = Contact
		fields = '__all__'





class VideoForm(forms.ModelForm):
	title = forms.CharField(label= 'العنوان',widget=forms.TextInput(attrs={'class': 'form-control'}), required = True)
	description = forms.CharField(label= 'الوصف',widget=forms.TextInput(attrs={'class': 'form-control'}), required = True)
	url = forms.CharField(label= 'عنوان URL',widget=forms.TextInput(attrs={'class': 'form-control'}), required = True)

	class Meta:
		model = Video
		fields = '__all__'





class UserTrainingForm(forms.ModelForm):
	user = forms.ModelChoiceField(label= 'المستخدم',widget=forms.Select(attrs={  'class':'form-control'}),queryset = User.objects.filter(is_active=True))
	training = forms.ModelChoiceField(label= 'الدورة',widget=forms.Select(attrs={  'class':'form-control'}),queryset = Training.objects.filter(statut=1))

	class Meta:
		model = UserTraining
		fields = (
			'user',
			'training',
				)


