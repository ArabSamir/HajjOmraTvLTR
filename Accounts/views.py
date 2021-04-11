from django.contrib.auth 			import login as login_auth, logout , authenticate
from django.contrib.auth.forms		import AuthenticationForm , PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.shortcuts 				import render , redirect,get_object_or_404 
from django.http                    import HttpResponse
from .models                        import User ,Contact , Content
from .forms                         import *
from django.contrib import messages
from django.utils.encoding          import force_text
import json 
from django.contrib 				import messages

from django.utils.encoding          import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http              import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader         import render_to_string
from django.core.mail               import EmailMessage
from datetime import date
from django.conf                    import settings


def signup(request):
	'''
		this function renders the service provider sign up page (registration)
	'''
	
	try:
		contact = Contact.objects.all()[0]
		content = Content.objects.all()[0]
		
	except Exception as e:
		print(e)
		contact = []
		content = []


	template_name = 'registration/signup.html'
	form = RegistrationForm()

	if request.method == 'POST':
		form = RegistrationForm(request.POST or None)
		if form.is_valid():
			try:
				
				instance = form.save()
				messages.success(request, f'مرحبا بك {instance.get_full_name()}')
				return redirect('index')
			except Exception as e:
				messages.error(request, 'error')
				return redirect('index')

	args = {'form' : form,
			'contact':contact,
			'content':content,
		}
	return render(request, template_name, args)




@login_required
def change_password(request):
	'''
		this function is to change the user password when user is logged in
	'''
	template_name = 'password_reset/change_password.html'

	try:
		contact = Contact.objects.all()[0]
		content = Content.objects.all()[0]
		
	except Exception as e:
		print(e)
		contact = []
		content = []
	if request.method == 'POST':
		form = ChangePasswordForm(data=request.POST , user = request.user)

		if form.is_valid():
			form.save()
			messages.success(request , 'Mot de passe Modifier')
			return redirect('change_password')
	   
		else:
		
			args =  {
					'form' : form ,
					}
			return render(request , template_name , args)

	else:
		form = ChangePasswordForm(user = request.user)

		args =  {
			'form' : form,
			'contact':contact,
			'content':content,
			 }

		return render(request , template_name , args)
	

def profile(request):
	template_name = 'registration/profile.html'
	user = get_object_or_404(User , pk=request.user.pk)
	profile = user.profile
	profile_form = ProfileUpdateForm(request.POST or None , request.FILES or None, instance=profile)
	user_form = UserUpdateForm(request.POST or None ,instance=user)
	
	try:
		contact = Contact.objects.all()[0]
		content = Content.objects.all()[0]
		
	except Exception as e:
		print(e)
		contact = []
		content = []

	if request.method == "POST":
		print(request.POST.get('birth_date'))
		if profile_form.is_valid() and user_form.is_valid():
			try:
				profile_form.save()
				user_form.save()
				messages.success(request , f'تم التعديل بنجاح')
				return redirect('profile')
			except Exception as e:
				messages.error(request , f'لم يتم إجراء تغييرات')
				return redirect('profile')

					
	args = {
		'profile_form':profile_form,
		'user_form':user_form,

		'contact':contact,
		'content':content,
	}

	return render(request , template_name , args)