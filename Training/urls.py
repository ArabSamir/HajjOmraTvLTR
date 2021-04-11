from django.urls import path, include, re_path
from .views import *
urlpatterns = [
	path('' , trainings , name='trainings' ),
	path('test/' , test , name='test' ),
	path('completed/' , completed , name='completed' ),
	path('my-trainings' , my_trainings , name='my_trainings' ),
	re_path(r'course/(?P<course_pk>[\w-]+)/$' , course_detail , name='course_detail' ),
	re_path(r'payment/(?P<pk>[\w-]+)/$' , payment , name='payment' ),
	re_path(r'active/(?P<pk>[\w-]+)/$' , active_training , name='active_training' ),
	re_path(r'deactivate/(?P<pk>[\w-]+)/$' , deactivate_training , name='deactivate_training' ),
	re_path(r'(?P<training_pk>[\w-]+)/$' , training_detail , name='training_detail' ),
]