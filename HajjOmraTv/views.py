from django.shortcuts import render , redirect
from Accounts.models import Contact , Content , Video
from Training.models import   Training
from Blog.models import Post
from django.core.mail               import send_mail
from Accounts.forms import ContactUsForm
from django.template.loader         import render_to_string
from django.contrib                 import messages
from django.conf					import settings

# Create your views here.

def index(request):
	template_name = 'pages/index.html'
	contact = Contact.objects.all()[0]
	content = Content.objects.all()[0]
	videos = Video.objects.all()
	posts = Post.objects.all()[:3]
	
	trainings = Training.objects.all()[:3]

	form = ContactUsForm(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			name = form.cleaned_data['name']
			email = form.cleaned_data['email']
			phone = form.cleaned_data['phone']
			text = form.cleaned_data['comments']
			
			message = render_to_string('email/contact_us_mail.html', {
			'name': name,
			'email': email,
			'phone': phone,
			'text': text,
			})
			try:
				send_mail( email, 'message', settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], html_message = message)
				messages.success(request , 'تم الإرسال بنجاح')
			except Exception as e:
				messages.error(request , f' {e}لم يتم إرسال الررسالة')
			
			return redirect('index')


	args = {
		'form':form,
		'contact':contact,
		'content':content,
		'videos':videos,
		'posts':posts,
		'trainings':trainings,
	}

	return render(request , template_name , args)