from django.shortcuts import render ,get_object_or_404 ,redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib 				import messages
from django.http                    import HttpResponse
import json 

from django.core.mail               import send_mail
from django.template.loader         import render_to_string
from django.conf					import settings
from Accounts.models import Contact,Content
from django.core.paginator import Paginator
from Blog.models import Post ,Category
from django.db.models import Q


# Create your views here.


def trainings (request):
	template_name = 'trainings.html'
	trainings = Training.objects.filter(statut=1).order_by('-created_on')
	last_trainings = trainings[:3]
	
	user = request.user
	if not user.is_anonymous :
		usertrainings = UserTraining.objects.filter(user=user)
		print(f'sdfhskdjfhskd {usertrainings}')
		
		if usertrainings.exists():
			for usertraining in usertrainings:
				trainings = trainings.exclude(pk=usertraining.training.pk) 

	contact = Contact.objects.all()[0]
	content = Content.objects.all()[0]

	# related_trainings = Training.filter(category=post.category).exclude(id=post.id)[:3]
	posts = Post.objects.all()
	last_posts = posts[:3]
	
	categories = Category.objects.all()[:5]

	if request.method == "GET" :
		keyword = request.GET.get('keyword')
		category =  request.GET.get('category')

		if keyword:
			trainings = trainings.filter(Q(title__icontains=keyword) | 
								 Q(description__icontains=keyword)| 
								 Q(content__icontains=keyword)
								 )

	paginator = Paginator(trainings, 6) # Show 25 contacts per page.
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	args = {
		'trainings':page_obj,
		'page_obj':page_obj,

		'last_trainings':last_trainings,
		'last_posts':last_posts,
		
		'categories':categories,
		'contact':contact,
		'content':content,
	}

	return render(request ,template_name, args)


def training_detail(request, training_pk):
	template_name = 'training_detail.html'
	training = get_object_or_404(Training , pk=training_pk)
	sections = Section.objects.filter(training=training).order_by('order')
	exists = False
	user = request.user
	
	if not user.is_anonymous :
		usertrainings = UserTraining.objects.filter(user=user)
		if usertrainings.filter(training=training).exists():
			exists = True

	trainings = Training.objects.all().order_by('-created_on')
	last_trainings = trainings[:3]


	contact = Contact.objects.all()[0]
	content = Content.objects.all()[0]



	try:
		
		active = UserTraining.objects.get( training=training,user=request.user  ).active
	except Exception as e:
		active = False	
	args = {
		'training':training,
		'sections':sections,
		'last_trainings':last_trainings,
	
		'exists':exists,
		'contact':contact,
		'content':content,
		'active':active,
	}

	return render(request ,template_name , args)


def course_detail(request , course_pk):
	template_name = 'course.html'
	contact = Contact.objects.all()[0]
	content = Content.objects.all()[0]
	
	course = get_object_or_404(Course , pk=course_pk)

	if not course.opened:

		try:
			user_training = UserTraining.objects.get( training=course.section.training,user=request.user  )
		except Exception as e:
			user_training = False
		if user_training:
			if not user_training.active  :
				messages.error(request , 'لم يتم تفعيل الدورة بعد')		
				return redirect('training_detail' ,  training_pk=course.section.training.pk)
		else:
			return redirect('payment' , pk=course.section.training.pk)
	args = {
		'course':course,
		'contact':contact,
		'content':content,
	}

	return render(request , template_name , args)



@login_required
def my_trainings(request):
	template_name = 'my_courses.html'
	user_trainings = UserTraining.objects.filter(user=request.user )
	
	paginator = Paginator(user_trainings, 6) # Show 25 contacts per page.
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	

	contact = Contact.objects.all()[0]
	content = Content.objects.all()[0]
	args = {
		'user_trainings': page_obj,
		'user_trainings': user_trainings,
		'page_obj': page_obj,
		'contact': contact,
		'content': content,
	} 

	return render(request , template_name , args)

@login_required
def payment(request , pk):
	template_name = "payment.html"
	training = get_object_or_404(Training , pk=pk)
	user = request.user
	training_exists =False
	if not user.is_anonymous :
	    
	    training_exists = UserTraining.objects.filter(training=training,user=user).exists()
	if training_exists :
		messages.error(request , 'لقد تم شراء هذه دورة من قبل')
		return redirect('training_detail' , training_pk=training.pk)
	sections = Section.objects.filter(training=training)
	contact = Contact.objects.all()[0]
	content = Content.objects.all()[0]

	if request.method == 'POST':
		data = json.loads(request.body)
		user_message = ''


		# email = data['details']['payer']['email_address']
		# exists = User.objects.filter(email=email).exists()
		# if exists:
		# 	user = User.objects.get(email=email)
		# 	training_exists = UserTraining.objects.filter(training=training,user=user).exists()
		# 	if training_exists :
		# 		messages.error(request , 'لقد تم شراء هذه دورة من قبل')
		# 		return redirect('trainings')
		# 	user_message = render_to_string('training_user_buy_email.html', {
		# 	'user': user,
		# 	'training': training,
		# 	})
		# else:
		# 	try:
		# 		name = data['details']['payer']['name']['given_name']
		# 		lastname = data['details']['payer']['name']['surname']
		# 		amount = data['details']['purchase_units'][0]['amount']['value']
		# 		payer_id = data['data']['payerID']
		# 		password = User.objects.make_random_password()
				
		# 		user = User(email=email , name =name ,lastname=lastname )
		# 		user.save()
		# 		user.set_password(password)
		# 		user.save()

		# 		user_message = render_to_string('training_new_user_buy_email.html', {
		# 		'user': user,
		# 		'password': password,
		# 		'training': training,
		# 		})
			
		# 		messages.success(request , 'user created successfully')
		# 	except Exception as e:
		# 		messages.error(request , f'user not created {e}')
		try:
			usertraining = UserTraining(user =user , training=training )
			usertraining.save()
			user_mail_subject = 'شكرا على شراء الدورة'
			seller_mail_subject = 'طلب شراء جديد'
			user_message = render_to_string('training_user_buy_email.html', {
			'user': user,
			'training': training,
			})
			seller_message = render_to_string('training_seller_buy_email.html', {
			'user': user,
			'training': training,
			'usertraining': usertraining,
			})
			send_mail( mail_subject, 'message', settings.EMAIL_HOST_USER, [email], html_message = user_message)
			send_mail( mail_subject, 'message', settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], html_message = seller_message)
			messages.success(request , 'لقد تم إرسال البريد الإلكتروني بنجاح')
			
			return redirect('completed')

		except Exception as e:
			messages.error(request , f'لم يتم إرسال البريد الإلكتروني  {e}')
			return redirect('trainings')
		

		

	args = {
		"training":training,
		'contact': contact,
		'content': content,
		'sections': sections,
	}

	return render (request , template_name , args)


def completed(request ):
	template_name = 'completed.html'
	contact = Contact.objects.all()[0]
	content = Content.objects.all()[0]

	args = {
		'contact': contact,
		'content': content,
	}

	return render(request , template_name , args)





def test(request):
	template_name = 'training_seller_buy_email.html'
	usertraining = UserTraining.objects.filter(pk=11)
	args = {
		'training':usertraining[0].training,
		'usertraining':usertraining[0],
	}

	return render(request , template_name,args)

@login_required
def active_training(request, pk ):

	user = request.user
	if user.email == settings.EMAIL_HOST_USER :
		try:
			usertraining = get_object_or_404(UserTraining , pk=pk)
			usertraining.active = True
			usertraining.save()
			message = render_to_string('training_active_email.html', {
			'user': user,
			'training': usertraining.training,
			'usertraining': usertraining,
			})
			mail_subject = 'تم تفعيل الدورة '
			send_mail( mail_subject, 'message', settings.EMAIL_HOST_USER, [usertraining.user.email], html_message = message)
			messages.success(request , 'تم التفعيل بنجاح')
		except Exception as e:
			messages.error(request , 'يوجد خطأ في التفعيل')
		

	return redirect('orders')

@login_required
def deactivate_training(request, pk):

	user = request.user
	if user.email == settings.EMAIL_HOST_USER :
		try:
			usertraining = get_object_or_404(UserTraining , pk=pk)
			usertraining.active = False
			usertraining.save()
			messages.success(request , 'تم التعطيل بنجاح')
		except Exception as e:
			messages.error(request , 'يوجد خطأ في التعطيل')
		

	return redirect('orders')