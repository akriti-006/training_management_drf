# urls.py
from django.urls import path
from .views import (
    ProgrammingLanguageListCreateView, ProgrammingLanguageDetailView,
    FrameworkListCreateView, FrameworkDetailView,
    CourseDataListCreateView, CourseDataDetailView,
    TrainingEnqueryListCreateView, TrainingEnqueryDetailView,
    CourseEnrollmentListCreateView, CourseEnrollmentDetailView,
    FeeInformationListCreateView, FeeInformationDetailView,
    CourseEnrollmentExtensionLogListCreateView, CourseEnrollmentExtensionLogDetailView
)

urlpatterns = [
    path('languages/', ProgrammingLanguageListCreateView.as_view(), name='language-list-create'),
    path('languages/<int:pk>/', ProgrammingLanguageDetailView.as_view(), name='language-detail'),

    path('frameworks/', FrameworkListCreateView.as_view(), name='framework-list-create'),
    path('frameworks/<int:pk>/', FrameworkDetailView.as_view(), name='framework-detail'),

    path('courses/', CourseDataListCreateView.as_view(), name='course-list-create'),
    path('courses/<int:pk>/', CourseDataDetailView.as_view(), name='course-data-detail'),

    path('enquiry/', TrainingEnqueryListCreateView.as_view(), name='enquiry-list-create'),
    path('enquiry/<int:pk>/', TrainingEnqueryDetailView.as_view(), name='enquiry-data-detail'),

    path('enrollments/', CourseEnrollmentListCreateView.as_view(), name='enrollment-list-create'),
    path('enrollments/<int:pk>/', CourseEnrollmentDetailView.as_view(), name='enrollment-detail'),

    path('fee-info/', FeeInformationListCreateView.as_view(), name='fee-info-list-create'),
    path('fee-info/<int:pk>', FeeInformationDetailView.as_view(), name='fee-info-detail'),

    path('extensions/', CourseEnrollmentExtensionLogListCreateView.as_view(), name='extension-list-create'),
    path('extensions/<int:pk>/', CourseEnrollmentExtensionLogDetailView.as_view(), name='extension-detail'),

]
