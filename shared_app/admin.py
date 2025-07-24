from django.contrib import admin
from .models import ProgrammingLanguage, Framework, CourseData

class ProgrammingLanguageAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'is_deleted']
    list_filter = ['is_deleted']
admin.site.register(ProgrammingLanguage, ProgrammingLanguageAdmin)


class FrameworkAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'language']
admin.site.register(Framework, FrameworkAdmin)


class CourseDataAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'duration_in_weeks', 'total_fee', 'created_by']
admin.site.register(CourseData, CourseDataAdmin)
