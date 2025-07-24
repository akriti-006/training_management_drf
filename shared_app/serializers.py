from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import ProgrammingLanguage, Framework, CourseData,TrainingEnquery, CourseEnrollment
from rest_framework import serializers
User = get_user_model()


class BaseSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Remove fields from the API response
        representation.pop('created_at', None)
        representation.pop('updated_at', None)
        representation.pop('is_deleted', None)
        representation.pop('created_by', None)
        
        return representation


class ProgrammingLanguageSerializer(BaseSerializer):
    class Meta:
        model = ProgrammingLanguage
        fields = '__all__'

    def validate_name(self, value):
        if ProgrammingLanguage.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError("Name already exists (case-insensitive).")
        return value


class FrameworkSerializer(BaseSerializer):
    language = serializers.PrimaryKeyRelatedField(queryset=ProgrammingLanguage.objects.all())

    class Meta:
        model = Framework
        fields = '__all__'

    def validate_name(self, value):
        if Framework.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError("Name already exists (case-insensitive).")
        return value

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation['language'] = ProgrammingLanguageSerializer(instance.language).data
        # representation.pop('created_at', None)
        # representation.pop('updated_at', None)
        # representation.pop('is_deleted', None)
        # representation.pop('created_by', None)

        return representation


class CourseDataSerializer(BaseSerializer):
    language = ProgrammingLanguageSerializer(read_only=True)

    class Meta:
        model = CourseData
        fields = '__all__'

    def validate_name(self, value):
        if CourseData.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError("Name already exists (case-insensitive).")
        return value

    def to_representation(self, instance):
        # First get the default representation
        representation = super().to_representation(instance)

        programming_data = instance.programming_languages.filter(is_deleted=False)
        programming_data = ProgrammingLanguageSerializer(programming_data, many=True).data

        framework_data = instance.frameworks.filter(is_deleted=False)
        framework_data = FrameworkSerializer(framework_data, many=True).data

        representation['programming_languages'] = programming_data
        representation['frameworks'] = framework_data

        return representation


class TrainingEnquerySerializer(BaseSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=CourseData.objects.filter(is_deleted=False))
    
    class Meta:
        model = TrainingEnquery
        fields = '__all__'
        
    def validate_email(self, value):
        if TrainingEnquery.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Email already exists (case-insensitive).")
        return value
    
    def to_representation(self, instance):
        
        representation = super().to_representation(instance)
        representation['course'] = CourseDataSerializer(instance.course).data
        representation['full_name'] = instance.get_full_name
        
        return representation

        
class CourseEnrollmentSerializer(BaseSerializer):
    course_detail = CourseDataSerializer(source='course', read_only= True)
    tran_enq = TrainingEnquerySerializer(read_only = True)
    class Meta:
        model = CourseEnrollment
        fields = '__all__'
        
    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        if end_date and start_date and end_date < start_date:
            raise serializers.ValidationError("End date must be after start date.")
        return data
    def get_course_status_display(self, obj):
        return obj.get_course_status_display()
