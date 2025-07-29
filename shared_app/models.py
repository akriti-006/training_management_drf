from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from training_management.utility.common_model import CommonModel
from training_management.utility.common_choices import (
    GENDER_CHOICES, STATUS_CHOICE, COURSE_STATUS_CHOICE
)

User = get_user_model()


class ProgrammingLanguage(CommonModel):
    '''
    
    '''
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'is_deleted'], name='unique_programming_language')
        ]

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()


class Framework(CommonModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    language = models.ForeignKey(ProgrammingLanguage, on_delete=models.CASCADE, related_name='frameworks')
    is_deleted = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'is_deleted'], name='unique_framework')
        ]

    def __str__(self):
        return self.name
    
    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()


class CourseData(CommonModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    duration_in_weeks = models.PositiveSmallIntegerField()
    total_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    programming_languages = models.ManyToManyField(ProgrammingLanguage, blank=True)
    frameworks = models.ManyToManyField(Framework, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'is_deleted'], name='unique_course')
        ]

    def __str__(self):
        return self.name
    
    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()


class TrainingEnquery(CommonModel):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    address = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    description = models.TextField()
    higher_qualification = models.CharField(max_length=100)
    course = models.ForeignKey(CourseData, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICE)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['email', 'course', 'is_deleted'], name='unique_enquiry')
        ]
    
    @property
    def get_full_name(self):
        return self.first_name + ''+ self.last_name
    
    def __str__(self):
        return self.first_name
    
    
class CourseEnrollment(CommonModel):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="student_enrollments")
    course = models.ForeignKey('CourseData', on_delete=models.CASCADE)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    course_status = models.CharField(max_length=100, choices=COURSE_STATUS_CHOICE)
    
    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError("End date must be after start date.")

    def __str__(self):
        return f"{self.student.email} enrolled in {self.course}"


class CourseEnrollmentExtensionLog(CommonModel):
    enrollment = models.ForeignKey(CourseEnrollment, on_delete=models.CASCADE)
    new_end_date = models.DateField()
    remark = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)


class FeeInformation(CommonModel):
    enrollment = models.ForeignKey(CourseEnrollment, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.enrollment.student} paid {self.amount_paid}"


class TeacherCourseEnrollmentMapping(CommonModel):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="teacher")
    course_enrollment = models.ForeignKey(CourseEnrollment, on_delete=models.CASCADE)
