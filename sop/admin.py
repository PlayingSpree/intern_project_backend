from django.contrib import admin

# Register your models here.
from .models import Session, Course, StepFile, Step, SopHistory

admin.site.register(Session)
admin.site.register(Course)
admin.site.register(StepFile)
admin.site.register(Step)
admin.site.register(SopHistory)
