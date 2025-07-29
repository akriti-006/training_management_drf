from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from .models import ProgrammingLanguage, Framework, CourseData,TrainingEnquery, CourseEnrollment
from rest_framework import serializers
User = get_user_model()

from datetime import datetime, timedelta


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

    training_enquery = serializers.PrimaryKeyRelatedField(
        queryset=TrainingEnquery.objects.filter(is_deleted=False),
        write_only=True
    )
    fee_amount = serializers.IntegerField(min_value=1, write_only=True)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = CourseEnrollment
        # fields = "__all__"
        fields = '__all__'
    
    def to_internal_value(self, data):
        print("📌 to_internal_value called")
        print("data ____________________________ : ", data)

        # step-1: fetch TrainingEnquery and check initial status
        obj = TrainingEnquery.objects.get(pk=data['training_enquery'])

        # if obj.status != "Enquiry":
        #     raise serializers.ValidationError({"training_enquery": "Training Enquery status must be Enquiry."})

        # update the status of existing TrainingEnquery
        obj.status = 'In Progress'
        obj.save()

        # Step-2: Check for student user, it's exising or new?
        first_name = obj.first_name
        last_name = obj.last_name
        email = obj.email

        #  Step-3 create User model object
        if user_obj := User.objects.filter(email=email).first():
            # user already exist
            is_new_user = False
            platform_msg = "Course assigned to the user as this is already exist."
            # send_new_course_email(obj, course_start_date, end_date)
        else:
            # new user
            is_new_user = True
            platform_msg = "Course started successfully!."
            email_msg = f"Hi {obj.first_name} {obj.last_name}, Your account is created for course : {obj.course.name}."

            # create user object
            user_obj = User.objects.create_user(
                first_name = first_name,
                last_name = last_name,
                email = email,
                password = data['password'],
                is_active = True
            )

            try:
                group = Group.objects.get(name='Student')
                user_obj.groups.add(group)
            except Group.DoesNotExist:
                print("Group does not exist.")
                # Handle the case where the group is not found

        # calculate course end_date
        course_duration = obj.course.duration_in_weeks
        start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
        end_date = start_date + timedelta(weeks=course_duration)

        data['student'] = user_obj.id
        data['course'] = obj.course.id
        data['end_date'] = str(end_date.date())
        data['course_status'] = 'In Progress'

        print("data : final ", data)

        print("data : final ", data)
        return super().to_internal_value(data)
        
    def validate(self, data):
        print("data ======================= : ", data)

        return data

    def to_representation(self, instance):
        """Customize output fields."""
        print("inside to_representation : ", instance)
        data = super().to_representation(instance)

        # Optionally customize student and course representations
        data['student'] = {
            "id": instance.student.id,
            "email": instance.student.email,
            "first_name": instance.student.first_name,
            "last_name": instance.student.last_name
        }

        data['course'] = {
            "id": instance.course.id,
            "name":instance.course.name
        }

        # Remove write-only fields from response
        data.pop('training_enquery', None)
        data.pop('fee_amount', None)
        data.pop('password', None)

        print("inside end od to_represent")

        return data
    
    def create(self, validated_data):

        print("B4 validated_data : ", validated_data)
        
        validated_data.pop('training_enquery')
        validated_data.pop('fee_amount')
        validated_data.pop('password')

        print("After : ", validated_data)
        # You can modify validated_data or perform extra actions

        instance = CourseEnrollment.objects.create(**validated_data)
        return instance
