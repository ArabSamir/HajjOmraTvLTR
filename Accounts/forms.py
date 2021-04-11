from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import (ReadOnlyPasswordHashField, 
										UserCreationForm,  
										UserChangeForm, AuthenticationForm, PasswordResetForm, SetPasswordForm , PasswordChangeForm)
from .models import User , Profile
from django.contrib.auth import authenticate, login , password_validation




class UserLoginForm(AuthenticationForm):
	def __init__(self, *args, **kwargs):
		super(UserLoginForm, self).__init__(*args, **kwargs)

	username = forms.EmailField(label= 'إسم المستخدم',widget=forms.TextInput(
		attrs={'class': 'form-control text-right text-right', 'type': 'email', 'name': 'email', '': 'Email'}))
	password = forms.CharField(label= 'كلمه السر',widget=forms.PasswordInput(
		attrs={'class': 'form-control text-right','autofocus': True ,'': 'Mot de passe', }))



class ResetPasswordForm(PasswordResetForm):
	def __init__(self, *args, **kwargs):
		super(PasswordResetForm, self).__init__(*args, **kwargs)

	email = forms.EmailField(label= 'إسم المستخدم',widget=forms.TextInput(
		attrs={'class': 'form-control text-right', 'type': 'email', '': 'Votre adresse e-mail :', }))
   


class PasswordSetForm(SetPasswordForm):
   
	new_password1 = forms.CharField(
		label= 'كلمة السر الجديدة',
		widget=forms.PasswordInput(attrs={'class': 'form-control text-right' , '': 'Le nouveau mot de passe :' , }),
		strip=False,
		help_text=password_validation.password_validators_help_text_html(),
	)
	new_password2 = forms.CharField(
		strip=False,
		label='تأكيد كلمة السر الجديدة',
		widget=forms.PasswordInput(attrs={'class': 'form-control text-right', '': 'Confirmez le nouveau mot de passe :'}),
	)


class ChangePasswordForm(PasswordChangeForm):
	def __init__(self, *args, **kwargs):
		super(PasswordChangeForm, self).__init__(*args, **kwargs)

	old_password = forms.CharField(
		label= 'كلمة السر القديمة',
		widget=forms.PasswordInput(attrs={'class': 'form-control text-right', '':"Ancien mot de passe :"}),
		strip=False,
		help_text=password_validation.password_validators_help_text_html(),
	)
	new_password1 = forms.CharField(
		strip=False,
		label= 'كلمة السر الجديدة',
		widget=forms.PasswordInput(attrs={'class': 'form-control text-right', '':"Le nouveau mot de passe :"}),
	)

	new_password2 = forms.CharField(
		strip=False,
		label='تأكيد كلمة السر الجديدة',
		widget=forms.PasswordInput(attrs={'class': 'form-control text-right', '':"Confirmez le nouveau mot de passe :"}),
	)

#--------------user creation form-----------------
class RegistrationForm(UserCreationForm):
	email = forms.EmailField(label= 'إسم المستخدم',required=True)
	name = forms.CharField(label= 'الإسم ',required=True)
	lastname = forms.CharField(label= 'اللقب',required=True)
	password1 = forms.CharField(
		label = 'كلمة السر',
		strip=False,
		widget=forms.PasswordInput,

	)
	password2 = forms.CharField(
		label = 'تأكيد كلمة السر الجديدة',
		strip=False,
		widget=forms.PasswordInput,

	)



	email.widget.attrs.update({'class': 'form-control text-right','autofocus': True ,'':'E-mail'})
	name.widget.attrs.update({'class': 'form-control text-right','autofocus': True ,'':'Prénom'})
	lastname.widget.attrs.update({'class': 'form-control text-right','autofocus': True ,'':'Nom'})
	password1.widget.attrs.update({'class': 'form-control text-right','autofocus': True, '':'Mot de passe'})
	password2.widget.attrs.update({'class': 'form-control text-right','autofocus': True , '':'Confirmé le Mot de passe' })
	
	class Meta:
		model = User
		fields = (
			'email', 
			'password1',
			'password2',
			'name',
			'lastname',
			)

	
	def clean_email(self):
		email = self.cleaned_data.get('email')
		users = User.objects.filter(email=email)
		if users.exists():
			if not users[0].is_active:
				try:
					send_email_confirmation('',users[0] ,self )
					
				except Exception as e:
					raise forms.ValidationError("E-mail n\'a pas été envoyé")
				raise forms.ValidationError("User  existe déjà verifier votre boite email pour activer ce compte.")
		return email


	

#--------------end user creation form-----------------



class RegisterForm(forms.ModelForm):
	password1 = forms.CharField(label=' كلمة السر ا',widget=forms.PasswordInput)
	password2 = forms.CharField(label='تأكيد كلمة السر الجديدة', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('email',)

	def clean_email(self):
		email = self.cleaned_data.get('email')
		qs = User.objects.filter(email=email)
		if qs.exists():
			raise forms.ValidationError("email is taken")
		return email

	def clean_password2(self):
		# Check that the two password entries match
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords don't match")
		return password2
	


class UserAdminCreationForm(forms.ModelForm):
	"""A form for creating new users. Includes all the required
	fields, plus a repeated password."""
	email = forms.EmailField(label= 'إسم المستخدم',required=True)
	name = forms.CharField(label= 'الإسم ',required=True)
	lastname = forms.CharField(label= 'اللقب',required=True)
	password1 = forms.CharField(
		label = 'كلمة السر',
		strip=False,
		widget=forms.PasswordInput,

	)
	password2 = forms.CharField(
		label = 'تأكيد كلمة السر الجديدة',
		strip=False,
		widget=forms.PasswordInput,

	)



	email.widget.attrs.update({'class': 'form-control text-right','autofocus': True ,'':'E-mail'})
	name.widget.attrs.update({'class': 'form-control text-right','autofocus': True ,'':'Prénom'})
	lastname.widget.attrs.update({'class': 'form-control text-right','autofocus': True ,'':'Nom'})
	password1.widget.attrs.update({'class': 'form-control text-right','autofocus': True, '':'Mot de passe'})
	password2.widget.attrs.update({'class': 'form-control text-right','autofocus': True , '':'Confirmé le Mot de passe' })
	
	class Meta:
		model = User
		fields = ('email','name' , 'lastname')

	def clean_password2(self):
		# Check that the two password entries match
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords don't match")
		return password2

	def save(self, commit=True):
		# Save the provided password in hashed format
		user = super(UserAdminCreationForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		if commit:
			user.save()
		return user


class UserAdminChangeForm(forms.ModelForm):
	"""A form for updating users. Includes all the fields on
	the user, but replaces the password field with admin's
	password hash display field.
	"""
	password = ReadOnlyPasswordHashField()
	email = forms.EmailField(label= 'إسم المستخدم',required=True)
	name = forms.CharField(label= 'الإسم ',required=True)
	lastname = forms.CharField(label= 'اللقب',required=True)
	



	email.widget.attrs.update({'class': 'form-control text-right','autofocus': True ,'':'E-mail'})
	name.widget.attrs.update({'class': 'form-control text-right','autofocus': True ,'':'Prénom'})
	lastname.widget.attrs.update({'class': 'form-control text-right','autofocus': True ,'':'Nom'})
	
	class Meta:
		model = User
		fields = ('email', 'password', 'is_active', 'is_admin' , 'name' , 'lastname')

	def clean_password(self):
		# Regardless of what the user provides, return the initial value.
		# This is done here, rather than on the field, because the
		# field does not have access to the initial value
		return self.initial["password"]





class ProfileUpdateForm(forms.ModelForm):
   
	choices = (
		('ذكر','ذكر'),
		('أنثى','أنثى')
		)
	birth_date = forms.DateField(label= 'تاريخ الميلاد' ,widget=forms.DateInput(format='%d/%m/%Y',attrs={'class': 'form-control datepicker'}), required = False )
	
	gender = forms.CharField(label= 'جنس ' ,widget=forms.Select(attrs={'class': 'form-control selectpicker'  } ,choices=choices ),required = False)
	

	class Meta:
		model = Profile
		fields = (
			'birth_date', 
			'gender',
			'image',
			)





class UserUpdateForm(forms.ModelForm):
	name = forms.CharField(label= 'الإسم' ,widget=forms.TextInput(attrs={'class': 'form-control text-right'}), required = True)
	lastname = forms.CharField(label= 'اللقب' ,widget=forms.TextInput(attrs={'class': 'form-control text-right'}), required = True)
	

	class Meta:
		model = User
		fields = (
			'name', 
			'lastname',
			)



class ContactUsForm (forms.Form):
	name = forms.CharField(label= 'الإسم' ,widget=forms.TextInput(attrs={'class': 'form-control ','placeholder': 'Nom',}), required = True)
	phone = forms.CharField(label= 'الهاتف' ,widget=forms.TextInput(attrs={'class': 'form-control ','placeholder': 'Tel',}), required = True)
	email = forms.EmailField(label= 'Email' ,widget=forms.EmailInput(attrs={'class': 'form-control ','placeholder': 'Email',}), required = True)
	comments = forms.CharField(label= 'التعليق' ,widget=forms.Textarea(attrs={'class': 'form-control','placeholder': 'Sujet',}), required = True)
	