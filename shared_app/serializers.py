from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from .models import (
    ProgrammingLanguage, Framework, 
    CourseData, TrainingEnquery, CourseEnrollment, FeeInformation,
    CourseEnrollmentExtensionLog
)
from django.db.models import Sum
from rest_framework import serializers
from datetime import datetime, timedelta
from training_management.utility.email_functionality import (
    send_welcome_email, send_enquiry_email,send_new_course_email,
    send_fee_submit_email, send_course_extension_email
)
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
        
    
    def to_representation(self, instance):
        
        representation = super().to_representation(instance)
        representation['course'] = CourseDataSerializer(instance.course).data
        representation['full_name'] = instance.get_full_name
        
        return representation
    
    def create(self, validated_data):
        instance = super().create(validated_data)
        send_enquiry_email(instance)

        return instance

        
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
        # step-1: fetch TrainingEnquery and check initial status
        obj = TrainingEnquery.objects.get(pk=data['training_enquery'])

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
            
        else:
            # new user
            is_new_user = True

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

         # Save data needed for email in serializer context
        data['student'] = user_obj.id
        data['course'] = obj.course.id
        data['end_date'] = str(end_date.date())
        data['course_status'] = 'In Progress'
        self.is_new_user = is_new_user

        print("data : ", data)
        return super().to_internal_value(data)
        
    def validate(self, data):
        print("data ======================= : ", data)

        return data

    def to_representation(self, instance):
        """Customize output fields."""
        data = super().to_representation(instance)

        # Optionally customize student and course representations
        data['student'] = {
            "id": instance.student.id,
            "first_name": instance.student.first_name,
            "last_name": instance.student.last_name,
            "email": instance.student.email
        }

        data['course'] = {
            "id": instance.course.id,
            "name":instance.course.name,
            "duration":instance.course.duration_in_weeks,
            "total_fees":instance.course.total_fee
        }

        # fees = FeeInformation.objects.filter(enrollment_id=instance, is_deleted=False)
        fees = instance.feeinformation_set.filter(enrollment_id=instance, is_deleted=False)
        serializer = FeeInformationSerializer(fees, many = True)

        total_paid = fees.aggregate(total=Sum('amount_paid'))['total'] or 0

        # Build the response
        data['fee_info'] = {
            "total_fees":instance.course.total_fee,
            "total_paid": total_paid,
            "installments": serializer.data
        }

        extension = instance.courseenrollmentextensionlog_set.filter(enrollment_id=instance, is_deleted=False)
        serializer = CourseEnrollmentExtensionLogSerializer(extension, many = True)
        # Build the response
        data['course_extension_log'] = serializer.data

        if extension.exists():
            latest_extension = extension.order_by('-created_at').first()
            if latest_extension and latest_extension.new_end_date:
                # data['end_date'] = str(instance.end_date)
                data['extended_end_date'] = str(latest_extension.new_end_date)
        # else:
        #     data['end_date'] = str(instance.end_date)

        return data
    
    def create(self, validated_data):
        training_enquery = validated_data.pop('training_enquery')
        fee_amount = validated_data.pop('fee_amount')
        password = validated_data.pop('password')
        is_new_user = self.is_new_user

        instance = CourseEnrollment.objects.create(**validated_data)

        if is_new_user:
            pass
            send_welcome_email(
                training_enquery,
                password,
                str(validated_data['start_date']),
                str(validated_data['end_date']),
                is_new_user
            )
        else:
            send_new_course_email(
                training_enquery,
                str(validated_data['start_date']),
                str(validated_data['end_date']),
            )

        # CourseEnrollment instance is saved, next step is to create FeeInformation
        new_data = {}
        new_data['enrollment'] = instance.id
        new_data['amount_paid'] = fee_amount
        new_data['created_by'] = instance.created_by.id

        serializer = FeeInformationSerializer(data = new_data)
        if serializer.is_valid():
            serializer.save()

        return instance


class FeeInformationSerializer(BaseSerializer):
    class Meta:
        model = FeeInformation
        fields = '__all__'

    def validate(self,data):
        enrollment = data.get('enrollment')
        amount_paid = data.get('amount_paid')

        obj = FeeInformation.objects.filter(enrollment=enrollment, is_deleted=False)
        total_amount_paid = obj.aggregate(total=Sum('amount_paid'))['total'] or 0

        course_fee = enrollment.course.total_fee

        pending_amount = course_fee - total_amount_paid

        if amount_paid > pending_amount:
            raise serializers.ValidationError(
                    {f"Your pending fee is {pending_amount}"}
                )

        if enrollment and amount_paid:
            total_amount = enrollment.course.total_fee
            if amount_paid > total_amount:
                raise serializers.ValidationError(
                    {"Amount paid cannot be greater than the course total fees."}
                )
        
        return data
    
    def create(self, validated_data):
        instance = FeeInformation.objects.create(**validated_data)
        print("Instance is created, going to send email")
        send_fee_submit_email(instance)
        print("Email sent")

        return instance

class CourseEnrollmentExtensionLogSerializer(BaseSerializer):
    class Meta:
        model = CourseEnrollmentExtensionLog
        fields = '__all__'

    def validate(self, data):
        enrollment = data.get('enrollment')
        new_end_date = data.get('new_end_date')

        if new_end_date < enrollment.start_date:
            raise serializers.ValidationError({
                'new_end_date': 'New end date cannot be earlier than the course start date.'
            })
        return data

    def create(self, validated_data):
        enrollment = validated_data['enrollment']
        remark = validated_data['remark']
        new_end_date = str(validated_data['new_end_date'])

        email_sent = False
        email_sent = send_course_extension_email(
            enrollment,
            remark,
            new_end_date
        )

        instance = CourseEnrollmentExtensionLog.objects.create(**validated_data)
        instance._email_sent = email_sent

        return instance
    