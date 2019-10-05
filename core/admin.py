from django.contrib import admin
from .models import *

# Register your models here.

class QuestionAdmin(admin.ModelAdmin):
    filter_horizontal = ['answers']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Test)
admin.site.register(StudentAnswer)
admin.site.register(StudentTest)
