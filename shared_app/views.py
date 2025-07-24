from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import (
    ProgrammingLanguage, Framework, CourseData,
    TrainingEnquery, CourseEnrollment
)
from .serializers import (
    ProgrammingLanguageSerializer,
    FrameworkSerializer, CourseDataSerializer,
    TrainingEnquerySerializer, CourseEnrollmentSerializer
)
from .utils import has_permission
from django.shortcuts import get_object_or_404
from django.http import Http404


class ProgrammingLanguageListCreateView(APIView):
    model = ProgrammingLanguage
    serializer_class = ProgrammingLanguageSerializer

    def get_queryset(self, request):
        is_deleted = request.query_params.get('is_deleted') == 'True'
        all = request.query_params.get('all') == 'True'

        if all:
            obj = self.model.objects.all()
        elif is_deleted:
            obj = self.model.objects.filter(is_deleted=True)
        else:
            obj = self.model.objects.filter(is_deleted=False)
        
        return obj

    def get(self, request):
        try:
            obj = self.get_queryset(request)
            serializer = self.serializer_class(obj, many=True)
            return Response({
            "message": "Programming language fetched successfully",
            "data": serializer.data,
            "total_item": obj.count()
        }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "message": str(e),
                "data": []
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    def post(self, request):
        try:
            data = request.data.copy()
            data['created_by'] = request.user.id
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "message": "Programming language created successfully",
                    "data": serializer.data
                }, status=status.HTTP_201_CREATED)
            return Response({
                "message": "Validation failed",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({
                "message": str(e),
                "data": None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class ProgrammingLanguageDetailView(APIView):
    model = ProgrammingLanguage
    serializer_class = ProgrammingLanguageSerializer
    
    def get_object(self, pk):
        try:
            obj = self.model.objects.get(pk=pk, is_deleted=False)
            return obj
        except self.model.DoesNotExist:
            raise Http404("Object does not exist")  

    def get(self, request, pk):
        try:
            obj = self.get_object(pk)
            if not has_permission(request.user, obj):
                return Response({
                    "message": "Permission denied",
                    "data": None
                    }, status=status.HTTP_403_FORBIDDEN)
            serializer = self.serializer_class(obj)
            return Response({
                "message": "Programming language fetched",
                    "data": serializer.data}, 
                    status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "message": str(e), 
                "data": {}
                }, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request, pk):
        try:
            data = request.data.copy()
            data['created_by'] = request.user.id
            obj = self.get_object(pk)
            if not has_permission(request.user, obj):
                return Response({
                    "message": "Permission denied", 
                    "data": None},
                    status=status.HTTP_403_FORBIDDEN)
            serializer = self.serializer_class(obj, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "Programming language updated", 
                     "data": serializer.data},
                     status=status.HTTP_200_OK)
            return Response({
                "message": "Validation failed", 
                "data": serializer.errors}, 
                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "message": str(e), 
                "data": {}}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request, pk):
        try:
            obj = self.get_object(pk)
            if not has_permission(request.user, obj):
                return Response({
                    "message": "Permission denied"}, 
                    status = status.HTTP_403_FORBIDDEN)
            obj.delete()
            return Response({
                "message": "Programming language deleted"}, 
                status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class FrameworkListCreateView(APIView):
    model = Framework
    serializer_class = FrameworkSerializer

    def get(self, request):
        try:
            is_deleted = request.query_params.get('is_deleted') == 'True'
            all = request.query_params.get('all') == 'True'

            if all:
                obj = self.model.objects.all()
            elif is_deleted:
                obj = self.model.objects.filter(is_deleted=True)
            else:
                obj = self.model.objects.filter(is_deleted=False)

            serializer = self.serializer_class(obj, many=True)
            return Response({
                "message": "Framework fetched successfully",
                "data": serializer.data,
                "total_item": obj.count()
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "message": str(e),
                "data": []
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            data = request.data.copy()
            data['created_by'] = request.user.id
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "message": "Framework created successfully",
                    "data": serializer.data
                }, status=status.HTTP_201_CREATED)
            return Response({
                "message": "Validation failed",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class FrameworkDetailView(APIView):
    model = Framework
    serializer_class = FrameworkSerializer

    def get_object(self, pk):
        try:
            obj = self.model.objects.get(pk=pk, is_deleted=False)
            return obj
        except self.model.DoesNotExist:
            raise Http404("Object does not exist")  

    def get(self, request, pk):
        try:
            framework = self.get_object(pk)
            if not has_permission(request.user, framework):
                return Response({
                    "message": "Permission denied"
                    }, status=status.HTTP_403_FORBIDDEN)
            serializer = self.serializer_class(framework)
            return Response({
                "message": "Framework fetched",
                    "data": serializer.data}, 
                    status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "message": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):
        try:
            data = request.data.copy()
            data['created_by'] = request.user.id
            obj = self.get_object(pk)
            if not has_permission(request.user, obj):
                return Response({
                    "message": "Permission denied"}, 
                    status=status.HTTP_403_FORBIDDEN)
            serializer = self.serializer_class(obj, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "message": "Framework updated", 
                    "data": serializer.data}, 
                    status=status.HTTP_200_OK)
            return Response({
                "message": "Validation failed", 
                "data": serializer.errors}, 
                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": str(e), "data": None}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        try:
            obj = self.get_object(pk)
            if not has_permission(request.user, obj):
                return Response({
                    "message": "Permission denied"}, 
                    status = status.HTTP_403_FORBIDDEN)
            obj.delete()
            return Response({
                "message": "Framework deleted"}, 
                status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "message": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class CourseDataListCreateView(APIView):
    model = CourseData
    serializer_class = CourseDataSerializer

    def get(self, request):
        try:
            is_deleted = request.query_params.get('is_deleted') == 'True'
            all = request.query_params.get('all') == 'True'

            if all:
                obj = self.model.objects.all()
            elif is_deleted:
                obj = self.model.objects.filter(is_deleted=True)
            else:
                obj = self.model.objects.filter(is_deleted=False)

            serializer = self.serializer_class(obj, many=True)
            return Response({
                "message": "Course fetched successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "message": str(e),
                "data": None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            data = request.data.copy()
            data['created_by'] = request.user.id
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                serializer.save(created_by=request.user) 
                return Response({
                    "message": "Course created successfully",
                    "data": serializer.data
                }, status=status.HTTP_201_CREATED)
            return Response({
                "message": "Validation failed",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({
                "message": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
class CourseDataDetailView(APIView):
    model = CourseData
    serializer_class = CourseDataSerializer

    def get_object(self, pk):
        try:
            obj = self.model.objects.get(pk=pk, is_deleted=False)
            return obj
        except self.model.DoesNotExist:
            raise Http404("Object does not exist")

    def get(self, request, pk):
        try:
            course = self.get_object(pk)
            if not has_permission(request.user, course):
                return Response({
                    "message": "Permission denied"}, 
                    status=status.HTTP_403_FORBIDDEN)
            serializer = self.serializer_class(course)
            return Response({
                "message": "Course fetched",
                    "data": serializer.data}, 
                    status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "message": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):
        try:
            data = request.data.copy()
            data['created_by'] = request.user.id
            obj = self.get_object(pk)
            if not has_permission(request.user, obj):
                return Response({
                    "message": "Permission denied"}, 
                    status=status.HTTP_403_FORBIDDEN)
            serializer = self.serializer_class(obj, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "message": "Course updated", 
                    "data": serializer.data}, 
                    status=status.HTTP_200_OK)
            return Response({
                "message": "Validation failed", 
                "data": serializer.errors}, 
                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        try:
            obj = self.get_object(pk)
            if not has_permission(request.user, obj):
                    return Response({
                        "message": "Permission denied"}, 
                        status = status.HTTP_403_FORBIDDEN)
            obj.delete()
            return Response({"message": "Course deleted"}, 
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TrainingEnqueryListCreateView(APIView):
    model = TrainingEnquery
    serializer_class = TrainingEnquerySerializer

    def get_queryset(self, request):
        obj = self.model.objects.filter(is_deleted=False)
        gender_param = request.query_params.get('gender')
        status_param = request.query_params.get('status')
        
        if gender_param:
            obj = obj.filter(gender__iexact=gender_param)
        if status_param:
            obj = obj.filter(status__iexact=status_param)
        
        return obj

    def get(self, request):
        try:
            obj = self.get_queryset(request)
            serializer = self.serializer_class(obj, many=True)
            return Response({"message": "Training Enquiries fetched",
                    "data": serializer.data,
                    "total_count": obj.count()}, 
                    status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            data = request.data.copy()
            data['created_by'] = request.user.id
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Enquiry created successfully",
                        "data": serializer.data},
                        status=status.HTTP_201_CREATED)
            return Response({"message": "Validation error",
                    "data": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class TrainingEnqueryDetailView(APIView):
    model = TrainingEnquery
    serializer_class = TrainingEnquerySerializer
    
    def get_object(self, pk):
        try:
            obj = self.model.objects.get(pk=pk, is_deleted=False)
            return obj
        except self.model.DoesNotExist:
            raise Http404("Object does not exist")
    
    def get(self, request, pk):
        try:
            obj = self.get_object(pk)
            if not has_permission(request.user, obj):
                return Response({
                    "message": "Permission denied"
                }, status=status.HTTP_403_FORBIDDEN)
            serializer = TrainingEnquerySerializer(obj)
            return Response({
                "message":"Training enquiry created successfully", 
                "data":serializer.data}, 
                status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message":str(e)}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self, request,pk):
        try:
            data = request.data.copy()
            data['created_by'] = request.user.id
            obj = self.get_object(pk)
            if not has_permission(request.user, obj):
                return Response({
                    "message": "Permission denied"
                }, status=status.HTTP_403_FORBIDDEN)
            serializer = self.serializer_class(obj, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "message":"Training enquiry updated successfully", 
                    "data": serializer.data},
                    status=status.HTTP_200_OK)
            return Response(serializer.errors, 
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": str(e)}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self, request, pk):
        try:
            obj = self.get_object(pk)
            if not has_permission(request.user, obj):
                return Response({
                    "message": "Permission denied",
                    "data": None
                }, status=status.HTTP_403_FORBIDDEN)
            obj.delete()
            return Response({
                "message": "Training enquiry deleted successfully"}, 
                status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message":str(e)}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class TrainingEnqueryStartListView(APIView):
    ...
        

class CourseEnrollmentListCreateView(APIView):
    model = CourseEnrollment
    serializer_class = CourseEnrollmentSerializer

    def get(self, request):
        try:
            obj = self.model.objects.all()
            serializer = self.serializer_class(obj, many = True)
            return Response({"message":"CourseEnrollment fetched successfully", 
                             "data":serializer.data},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message":str(e),
                             "data":None},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def post(self, request):
        try:
            data = request.data.copy()
            data['created_by'] = request.user.id
            serializer = CourseEnrollmentSerializer(data = data)
            if serializer.is_valid():
                serializer.save(created_by = request.user)
                return Response({"message":"Course Enrollment created successfully","data":serializer.data}, status=status.HTTP_201_CREATED)
            return Response({"message":"validation error","data":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message":str(e),"data":None}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class CourseEnrollmentDetailView(APIView):
    def get_object(self, pk):
        return get_object_or_404(CourseEnrollment,pk=pk)
    
    def get( self, request,pk):
        try:
            obj = self.get_object(pk)
            if not has_permission(request.user, obj):
                return Response({
                    "message": "Permission denied",
                    "data": None
                }, status=status.HTTP_403_FORBIDDEN)
            serializer = CourseEnrollmentSerializer(obj)
            return Response({"message": "Course Enrollment Created successfully", "data": serializer.data}, status= status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": str(e), "data": None}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self, request, pk):
        try:
            obj = self.get_object(pk)
            if not has_permission(request.user, obj):
                return Response({
                    "message": "Permission denied",
                    "data": None
                }, status=status.HTTP_403_FORBIDDEN)
            serializer = CourseEnrollmentSerializer(obj, data = request.data, partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"Course Enrollment updated successfully", "data": serializer.data},status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": str(e), "data": None}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self, request, pk):
        try:
            obj = self.get_object(pk)
            if not has_permission(request.user, obj):
                return Response({
                    "message": "Permission denied",
                    "data": None
                }, status=status.HTTP_403_FORBIDDEN)
            obj.delete()
            return Response({"message": "Course Enrollment deleted successfully", "data": None}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message":str(e), "data": None}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        