# urls.py
from django.urls import path
from .views import (
    ProgrammingLanguageListCreateView, ProgrammingLanguageDetailView,
    FrameworkListCreateView, FrameworkDetailView,
    CourseDataListCreateView, CourseDataDetailView,
    TrainingEnqueryListCreateView, TrainingEnqueryDetailView,
    CourseEnrollmentListCreateView, CourseEnrollmentDetailView
)

urlpatterns = [
    path('languages/', ProgrammingLanguageListCreateView.as_view(), name='language-list-create'),
    path('languages/<int:pk>/', ProgrammingLanguageDetailView.as_view(), name='language-detail'),

    path('frameworks/', FrameworkListCreateView.as_view(), name='framework-list-create'),
    path('frameworks/<int:pk>/', FrameworkDetailView.as_view(), name='framework-detail'),

    path('courses/', CourseDataListCreateView.as_view(), name='course-list-craete'),
    path('courses/<int:pk>/', CourseDataDetailView.as_view(), name='course-data-detail'),

    path('enquiry/', TrainingEnqueryListCreateView.as_view(), name='enquiry-list-craete'),
    path('enquiry/<int:pk>/', TrainingEnqueryDetailView.as_view(), name='enquiry-data-detail'),

    path('enrollments/', CourseEnrollmentListCreateView.as_view(), name='enrollment-list-craete'),
    path('enrollments/<int:pk>/', CourseEnrollmentDetailView.as_view(), name='enrollment-data-detail'),

]
