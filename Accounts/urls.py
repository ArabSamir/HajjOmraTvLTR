from django.urls                import path,re_path , include
from Accounts.views             import *
from django.contrib.auth.views import ( LoginView,
                                        LogoutView, 
                                        PasswordResetView, 
                                        PasswordResetCompleteView,  
                                        PasswordChangeDoneView, 
                                        PasswordResetConfirmView, 
                                        PasswordResetDoneView,
                                        PasswordChangeView
                                        )
from django.conf                    import settings
from Accounts.models import Contact , Content

try:
    contact = Contact.objects.all()[0]
    content = Content.objects.all()[0]
    
except Exception as e:
    print(e)
    contact = []
    content = []


args = {
    'contact':contact,
    'content':content,
}
urlpatterns = [

	
    path('login/', LoginView.as_view(template_name='registration/login.html', form_class=UserLoginForm ,extra_context=args)  , name='login' ),
    path('logout/', LogoutView.as_view() , name='logout'),
    
    path('signup/', signup, name='signup'),
    path('profile/', profile, name='profile'),
    path('change-password/', change_password, name='change_password'),
    
    path('reset-password/', PasswordResetView.as_view(template_name='password_reset/password_reset_form.html',form_class =ResetPasswordForm, html_email_template_name='email/password_reset_email.html',subject_template_name='email/password_reset_subject.txt',from_email = settings.EMAIL_HOST_USER ,extra_context=args) ,  name='password_reset'),
    path('reset-password/done/', PasswordResetDoneView.as_view(template_name = 'password_reset/password_reset_done.html',extra_context=args)  , name='password_reset_done'),
    re_path(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/', PasswordResetConfirmView.as_view(template_name = 'password_reset/password_reset_confirm.html',form_class = PasswordSetForm,extra_context=args)  , name='password_reset_confirm' ),
    path('reset-password/complete/', PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_complete.html',extra_context=args)  , name='password_reset_complete'),

   	
    ]   