from django.shortcuts import render , get_object_or_404 , redirect
from .models import *
from django.core.paginator import Paginator
from django.contrib 				import messages
from .forms import *
from Accounts.models import Contact , Content
from django.db.models import Q
# Create your views here.

def post_detail(request , pk):
	template_name = 'post_detail.html'

	post = get_object_or_404(Post , pk=pk) 
	posts = Post.objects.filter(statut=1).order_by('-created_on')
	last_posts = posts[:3]
	related_posts = posts.filter(category=post.category).exclude(id=post.id)[:3]
	categories = Category.objects.all()[:5]


	contact = Contact.objects.all()[0]
	content = Content.objects.all()[0]

	comments = Comment.objects.filter(post=post)
	nb_comments = comments.count()


	form = CommentForm(request.POST or None)	
	if request.method == "POST":
		if form.is_valid():
			try:
				comment =form.save(commit=False)
				comment.creator = request.user
				comment.post = post
				comment.save()
				messages.success(request, 'تم إنشاء التعليق بنجاح')
			except Exception as e:
				messages.error(request, f'لم يتم إنشاء التعليق {e}')
							
			return redirect('post_detail' , pk=pk)

	args ={
		'nb_comments':nb_comments,
		'comments':comments,
		'categories':categories,
		'post':post,
		'form':form,
		'last_posts':last_posts,
		'related_posts':related_posts,
		'contact':contact,
	    'content':content,
	}

	return render(request , template_name , args)

def blog(request):
	template_name = 'blog.html'

	posts = Post.objects.filter(statut=1).order_by('-created_on')
	last_posts = posts[:3]


	if request.method == "GET" :
		keyword = request.GET.get('keyword')
		category =  request.GET.get('category')

		if keyword:
			posts = posts.filter(Q(title__icontains=keyword) | 
								 Q(description__icontains=keyword)| 
								 Q(content__icontains=keyword)| 
								 Q(category__category_name__icontains=keyword)|
								 Q(author__lastname__icontains=keyword)|
								 Q(author__name__icontains=keyword)
								 )
		if category:
			posts = posts.filter(category__id=int(category))

	paginator = Paginator(posts, 3) # Show 25 contacts per page.
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	contact = Contact.objects.all()[0]
	content = Content.objects.all()[0]
	categories = Category.objects.all()[:5]
	

	args = {
		'last_posts':last_posts,
		'posts':page_obj,
		'page_obj':page_obj,
	    'categories':categories,
		
		'contact':contact,
	    'content':content,
	}

	return render(request , template_name , args)