from django.contrib import admin
from .models import ProgrammingLanguage, Framework, CourseData, TrainingEnquery, CourseEnrollment, FeeInformation

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


class TrainingEnqueryAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name','email','gender','is_deleted']
    list_filter = ('gender' , 'status')
    fieldsets = [
        (
            "Basic Details",
            {
                "fields": ["first_name", "last_name", "address", "email", "phone", "gender", "description", "higher_qualification"],
            },
        ),
        (
            "Course Details",
            {
                "classes": ["open"],
                "fields": ["course", "status"]
            }
        )
    ]
admin.site.register(TrainingEnquery, TrainingEnqueryAdmin)


class CourseEnrollmentAdmin(admin.ModelAdmin):
    list_display =['id', 'course__name', 'start_date', 'end_date', 'course_status']
    
    # def student_name(self, obj):
    #     name = obj.student.get_full_name()
    #     return name
    
    # student_name.short_description = 'Stu Name'
    
admin.site.register(CourseEnrollment,CourseEnrollmentAdmin)


class FeeInformationAdmin(admin.ModelAdmin):
    list_display = ['id','enrollment','amount_paid', 'is_deleted', 'created_by']
admin.site.register(FeeInformation, FeeInformationAdmin)
