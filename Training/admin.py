from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(Training)
admin.site.register(Section)
admin.site.register(Course)
@admin.register(UserTraining)
class UserTrainingAdmin(admin.ModelAdmin):
	list_display  = ('pk','user','training','purchase_date','active',)
	ordering = ("pk", "user")