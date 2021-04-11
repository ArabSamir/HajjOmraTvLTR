from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):

	text = forms.CharField(label= 'التعليق' ,widget=forms.Textarea(attrs={'class': 'form-control text-right','rows' :"10" ,'cols' :"1000"}), required = True)


	class Meta():
		model = Comment
		fields = ('text',)