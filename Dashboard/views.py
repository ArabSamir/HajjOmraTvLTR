from django.shortcuts import render ,get_object_or_404 ,redirect
from Training.models import *
from Blog.models import *
from .forms import *
from django.contrib 				import messages
from django.contrib.auth.decorators import user_passes_test
from Accounts.models import User
from Accounts.forms import UserAdminChangeForm ,ProfileUpdateForm , UserAdminCreationForm
def is_admin(user):
	
	if user.is_authenticated and user.is_admin:
		return  True
	else:
		return False


@user_passes_test(is_admin)
def dashboard(request):
	template_name = 'pages/dashboard.html'

	args = {

	}

	return render(request, template_name , args)



@user_passes_test(is_admin)
def all_trainings(request):
	template_name = 'training/all.html'
	trainings = Training.objects.all()
	training_form = TrainingForm(request.POST or None  , request.FILES or None)
	if request.method =="POST":
		if training_form.is_valid():
			instance = training_form.save()
			messages.success(request , 'تم التعديل بنجاح')
			return redirect('dash_training_detail' , pk=instance.pk)
	
	args = {
		'trainings':trainings,
		'training_form':training_form,
	}

	return render(request, template_name , args)

@user_passes_test(is_admin)
def add_training(request):
	template_name = 'training/add_training.html'
	form = TrainingForm(request.POST or None , request.FILES or None)
	if request.method == 'POST':

		if form.is_valid():
			try:
				instance = form.save()
				messages.success(request, 'تمت الإضافة بنجاح' )
				return redirect('dash_training_detail' , pk=instance.pk)
			except Exception as e:
				messages.error(request, f'لم يتم  إضافة الدورة {e}')

	args = {
		'form':form,
	}
	return render(request , template_name , args)	



@user_passes_test(is_admin)
def dash_training_detail(request , pk):
	template_name = "training/dash_training_detail.html"
	training = get_object_or_404(Training , pk=pk)
	training_form = TrainingForm(request.POST or None ,request.FILES or None, instance=training)
	section_form = SectionForm(request.POST or None , pk , training_id = pk)
	if request.method =='POST':
		if 'training' in request.POST:

			if training_form.is_valid():
				training_form.save()
				messages.success(request , 'تم التعديل بنجاح')
				return redirect('dash_training_detail' , pk=pk)

		if 'add_section' in request.POST:
			if section_form.is_valid():
				instance = section_form.save(commit=False)
				instance.training = training
				instance.save()
				messages.success(request, 'تم إضافة الوحدة بنجاح')
				return redirect('dash_section_detail' , pk=instance.pk)
				
	args = {
		'form':training_form,
		'section_form':section_form,
		'training':training,
	}

	return render(request , template_name , args)


@user_passes_test(is_admin)
def del_training(request , pk):
	training = get_object_or_404(Training , pk=pk)
	try:
		training.delete()
		messages.success(request, 'تم حذف الدورة بنجاح')
		return redirect('all_trainings')
	except Exception as e:
		messages.error(request, f'لم يتم حذف الدورة  {e}')
		return redirect('all_trainings')
	


@user_passes_test(is_admin)
def dash_section_detail(request , pk):
	template_name = "training/dash_section_detail.html"
	section = get_object_or_404(Section , pk=pk)
	form = SectionForm(request.POST or None , instance=section , training_id = section.training.pk)
	course_form = CourseForm(request.POST or None ,  section_id=section.id)
	if request.method =='POST':
		if 'section' in request.POST:

			if form.is_valid():
				form.save()
				messages.success(request , 'تم التعديل بنجاح')
				return redirect('dash_section_detail' , pk=pk)

		if 'add_course' in request.POST:
			if course_form.is_valid():
				instance = course_form.save(commit=False)
				instance.section = section
				instance.save()
				messages.success(request, 'تم الإضافة  بنجاح')
				return redirect('dash_section_detail' , pk=pk)
						


	args = {
		'form':form,
		'section':section,
		'course_form':course_form,
	}

	return render(request , template_name , args)



@user_passes_test(is_admin)
def del_section(request , pk):
	section = get_object_or_404(Section , pk=pk)
	training = section.training
	try:
		section.delete()
		messages.success(request, 'تم حذف الوحدة بنجاح')
		return redirect('dash_training_detail' , pk=training.pk )
	except Exception as e:
		messages.error(request, f'لم يتم حذف الوحدة  {e}')
		return redirect('dash_training_detail' , pk=training.pk )



@user_passes_test(is_admin)
def dash_course_detail(request , pk):
	template_name = "training/dash_course_detail.html"
	course = get_object_or_404(Course , pk=pk)
	form = CourseForm(request.POST or None , instance=course , section_id=course.section.id)
	if request.method =='POST':
	
		if form.is_valid():
			form.save()
			messages.success(request , 'تم التعديل بنجاح')
			return redirect('dash_course_detail' , pk=pk)

					


	args = {
		'form':form,
		'course':course,
	}

	return render(request , template_name , args)



@user_passes_test(is_admin)	
def del_course(request , pk):
	course = get_object_or_404(Course , pk=pk)
	section = course.section
	try:
		course.delete()
		messages.success(request, 'تم حذف الدرس بنجاح')
		return redirect('dash_section_detail' , pk=section.pk )
	except Exception as e:
		messages.error(request, f'لم يتم حذف الوحدة  {e}')
		return redirect('dash_section_detail' , pk=section.pk )
	

@user_passes_test(is_admin)
def orders(request):
	template_name  = 'training/orders.html'
	orders = UserTraining.objects.all().order_by('purchase_date')
	form = UserTrainingForm(request.POST or None)
	if request.method == "POST":
		if form.is_valid():
			try:

				form.save()
				messages.success(request, 'تمت الإضافة بنجاح')
			except Exception as e:
				messages.error(request, f'لم تتم الإضافة {e}')

			return redirect('orders' )

	args = {
		'orders':orders,
		'form':form,
	}

	return render(request , template_name , args)





@user_passes_test(is_admin)
def all_posts(request ):
	template_name = "blog/posts.html"
	posts = Post.objects.all()
	form = PostForm(request.POST or None , request.FILES or None)
	if request.method=='POST':
		if form.is_valid():
			instance = form.save(commit=False)
			instance.author = request.user
			instance.save()
			messages.success(request, 'تمت الإضافة بنجاح')
			return redirect('posts'  )
		


	args = {
		'posts':posts,
		'form':form,
	}

	return render(request , template_name , args)


@user_passes_test(is_admin)
def dash_post_detail(request , pk):
	template_name = "blog/dash_post_detail.html"
	post = get_object_or_404(Post , pk=pk)
	form = PostForm(request.POST or None , request.FILES or None, instance=post)
	if request.method =='POST':
	
		if form.is_valid():
			form.save()
			messages.success(request , 'تم التعديل بنجاح')
			return redirect('dash_post_detail' , pk=pk)
	


	args = {
		'form':form,
		'post':post,
	}

	return render(request , template_name , args)



@user_passes_test(is_admin)	
def del_post(request , pk):
	post = get_object_or_404(Post , pk=pk)
	try:
		post.delete()
		messages.success(request, 'تم حذف الدرس بنجاح')
	except Exception as e:
		messages.error(request, f'لم يتم حذف المقال  {e}')
	
	return redirect('all_posts')


@user_passes_test(is_admin)
def categories(request):
	template_name = 'blog/categories.html'
	categories = Category.objects.all()
	form = CategoryForm(request.POST or None )
	if request.method == "POST" :
		if form.is_valid():
			instance = form.save()
			messages.success(request, 'تمت الإضافة بنجاح')
			return redirect('category_detail' , pk=instance.pk)
	args = {
		'categories':categories,
		'form':form,
	}

	return render(request , template_name , args)

@user_passes_test(is_admin)
def category_detail(request , pk):
	template_name = 'blog/category_detail.html'
	category = get_object_or_404(Category , pk=pk)
	form = CategoryForm(request.POST or None , instance=category)
	
	if request.method == "POST" :
		if form.is_valid():
			form.save()
			messages.success(request , 'تم التعديل بنجاح')

	args = {
		'category':category,
		'form':form,
	}

	return render(request , template_name , args)
	

@user_passes_test(is_admin)	
def del_category(request , pk):
	category = get_object_or_404(Category , pk=pk)
	try:
		category.delete()
		messages.success(request, 'تم حذف الفئة بنجاح')
	except Exception as e:
		messages.error(request, f'لم يتم حذف المقال  {e}')
	
	return redirect('categories')
	

@user_passes_test(is_admin)
def comments(request):
	template_name = 'blog/comments.html'
	comments = Comment.objects.all()

	args = {
		'comments':comments,
	}

	return render(request , template_name , args)

@user_passes_test(is_admin)	
def del_comment(request , pk):
	comment = get_object_or_404(Comment , pk=pk)
	try:
		comment.delete()
		messages.success(request, 'تم حذف التعليق بنجاح')
	except Exception as e:
		messages.error(request, f'لم يتم حذف التعليق  {e}')
	
	return redirect('comments')
	

@user_passes_test(is_admin)
def add_post(request):
	template_name = 'blog/add_post.html'
	form = PostForm(request.POST or None , request.FILES or None)
	if request.method == 'POST':
			
		if form.is_valid():
			try:
				instance = form.save(commit=False)
				instance.author = request.user
				instance.save()
				messages.success(request, 'تمت الإضافة بنجاح' )
				return redirect('dash_post_detail' , pk=instance.pk)
			except Exception as e:
				messages.error(request, f'لم يتم  إضافة الدورة {e}')

	args = {
		'form':form,
	}
	return render(request , template_name , args)

@user_passes_test(is_admin)
def content(request):
	template_name = 'parameters/content.html'
	instance = Content.objects.all()[0]
	form = ContentForm(request.POST or None , request.FILES or None , instance=instance)
	if request.method == 'POST':
			
		if form.is_valid():
			try:
				instance = form.save()
				messages.success(request, 'تم التعديل بنجاح' )
				return redirect('content')
			except Exception as e:
				messages.error(request, f'لم يتم  إضافة الدورة {e}')

	args = {
		'form':form,
	}
	return render(request , template_name , args)

@user_passes_test(is_admin)
def contact(request):
	template_name = 'parameters/contact.html'
	instance = Contact.objects.all()[0]
	form = ContactForm(request.POST or None , request.FILES or None , instance=instance)
	if request.method == 'POST':
			
		if form.is_valid():
			try:
				instance = form.save()
				messages.success(request, 'تم التعديل بنجاح' )
				return redirect('contact')
			except Exception as e:
				messages.error(request, f'لم يتم  إضافة الدورة {e}')

	args = {
		'form':form,
	}
	return render(request , template_name , args)


@user_passes_test(is_admin)
def videos(request):
	template_name = 'parameters/videos.html'
	videos = Video.objects.all()
	form = VideoForm(request.POST or None , request.FILES or None )
	if request.method == "POST":
		if form.is_valid():
			try:
				instance = form.save()
				messages.success(request, 'تمت الإضافة بنجاح' )
				return redirect('videos')
			except Exception as e:
				messages.error(request, f'لم يتم  إضافة  الفيديو  {e}')
	args = {
		'form': form,
		'videos': videos,
	}

	return render(request , template_name , args)


@user_passes_test(is_admin)
def video_detail(request , pk):
	template_name = 'parameters/video_detail.html'
	instance = get_object_or_404(Video , pk=pk)
	form = VideoForm(request.POST or None , request.FILES or None , instance=instance)
	if request.method == "POST":
		if form.is_valid():
			try:
				instance = form.save()
				messages.success(request, 'تم التعديل بنجاح' )
				return redirect('video_detail' , pk=pk)
			except Exception as e:
				messages.error(request, f'لم يتم  التعديل  {e}')
	args = {
		'form': form,
		'instance': instance,
	}

	return render(request , template_name , args)


@user_passes_test(is_admin)	
def del_video(request , pk):
	video = get_object_or_404(Video , pk=pk)
	try:
		video.delete()
		messages.success(request, 'تم حذف الفيديو بنجاح')
	except Exception as e:
		messages.error(request, f'لم يتم حذف الفيديو  {e}')
	
	return redirect('videos')
	



def users(request):
	template_name = 'accounts/users.html'
	users = User.objects.all()
	form = UserAdminCreationForm(request.POST or None)

	if request.method == 'POST':
		if form.is_valid() and profile_form.is_valid():
			form.save()
			return redirect('user_detail' , pk=instance.pk)

	args = {
		'users':users,
		'form':form,
	}
	return render(request , template_name , args)

def user_detail(request , pk):
	template_name = 'accounts/user_detail.html'
	instance = get_object_or_404(User , pk=pk)
	form = UserAdminChangeForm(request.POST or None , instance=instance)
	profile_form = ProfileUpdateForm(request.POST or None , request.FILES or None  , instance=instance.profile)
	if request.method == 'POST':
		if form.is_valid() and profile_form.is_valid():
			form.save()
			profile_form.save()

			return redirect('user_detail' , pk=pk)

	args = {
		'user':instance,
		'form':form,
		'profile_form':profile_form,
	}
	return render(request , template_name , args)


def del_user(request , pk):
	user = get_object_or_404(User , pk=pk)
	try:
		user.delete()
		messages.success(request, 'تم الحذف  بنجاح')
	except Exception as e:
		messages.error(request, f'لم يتم حالذف   {e}')
	
	return redirect('users')
	