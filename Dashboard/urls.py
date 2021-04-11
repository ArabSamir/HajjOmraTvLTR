from django.urls import path,include ,re_path
from .views import *


urlpatterns = [
    path('', dashboard , name='dashboard' ),
    path('trainings/all/', all_trainings , name='all_trainings' ),
    path('trainings/add/', add_training , name='add_training' ),
    path('orders/all/', orders , name='orders' ),
    re_path(r'training/section/(?P<pk>[\w-]+)/$', dash_section_detail , name='dash_section_detail' ),
    re_path(r'training/(?P<pk>[\w-]+)/$', dash_training_detail , name='dash_training_detail' ),
    re_path(r'training/(?P<pk>[\w-]+)/del/$', del_training , name='del_training' ),
    re_path(r'training/section/(?P<pk>[\w-]+)/del/$', del_section , name='del_section' ),
    re_path(r'training/section/course/(?P<pk>[\w-]+)/$', dash_course_detail , name='dash_course_detail' ),
    re_path(r'training/section/course/(?P<pk>[\w-]+)/del/$', del_course , name='del_course' ),

    
    path('posts/add/', add_post , name='add_post' ),
    path('posts/all/', all_posts , name='all_posts' ),
    re_path(r'post/(?P<pk>[\w-]+)/$', dash_post_detail , name='dash_post_detail' ),
    re_path(r'post/(?P<pk>[\w-]+)/del/$', del_post , name='del_post' ),

    path('categories/all/', categories , name='categories' ),
    re_path(r'category/(?P<pk>[\w-]+)/$', category_detail , name='category_detail' ),
    re_path(r'category/(?P<pk>[\w-]+)/del/$', del_category , name='del_category' ),

    path('comments/all/', comments , name='comments' ),
    re_path(r'comment/(?P<pk>[\w-]+)/del/$', del_comment , name='del_comment' ),
    
    path('content/', content , name='content' ),
    path('contact/', contact , name='contact' ),

    path('videos/all/', videos , name='videos' ),

    re_path(r'video/(?P<pk>[\w-]+)/$', video_detail , name='video_detail' ),
    re_path(r'video/(?P<pk>[\w-]+)/del/$', del_video , name='del_video' ),

    path('users/all/', users , name='users' ),
    re_path(r'user/(?P<pk>[\w-]+)/$', user_detail , name='user_detail' ),
    re_path(r'user/(?P<pk>[\w-]+)/del/$', del_user , name='del_user' ),
]
