from django.contrib import admin

# Register your models here.
from .models import Post, Course, StepFile, Step, SopHistory

admin.site.register(Post)
admin.site.register(Course)
admin.site.register(StepFile)
admin.site.register(Step)
admin.site.register(SopHistory)
