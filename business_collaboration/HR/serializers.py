from rest_framework import serializers
from .models import Personal, Vacancy, VisitHistory, VisitHistoryComment, VacationRequest, Sticker, Award
from accounts.models import UserProfile


class UserProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['full_name', 'phone_number', 'email', 'image_user']


class UserProfileSimpleSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['full_name', 'image_user']


class PersonalProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = Personal
        fields = ['id', 'employee', 'phone_number', 'post', 'department', 'date_of_employment', 'image_user',
                  'marital_status', 'address', 'emergency_contacts', 'education', 'university_college', 'skills',
                  'employment_type', 'passport_number', 'health_history']


class PersonalCreateSerializers(serializers.ModelSerializer):
    # employee = UserProfileSerializers(many=True)

    class Meta:
        model = Personal
        fields = ['employee', 'post', 'department', 'marital_status', 'address', 'emergency_contacts',
                  'education', 'university_college', 'skills', 'employment_type', 'passport_number', 'health_history',
                  'pay']


class PersonalUpdateDeleteSerializers(serializers.ModelSerializer):
    employee = UserProfileSerializers()

    class Meta:
        model = Personal
        fields = ['employee', 'post', 'department', 'marital_status', 'address', 'emergency_contacts',
                  'education', 'university_college', 'skills', 'employment_type', 'passport_number', 'health_history',
                  'pay']

    def update(self, instance, validated_data):
        employee_data = validated_data.pop('employee', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if employee_data:
            user_profile = instance.employee
            for attr, value in employee_data.items():
                setattr(user_profile, attr, value)
            user_profile.save()
        instance.save()
        return instance


class PersonalListSerializers(serializers.ModelSerializer):
    employee = UserProfileSerializers()

    class Meta:
        model = Personal
        fields = ['id', 'employee', 'post', 'department', 'date_of_employment']


class ProfileSerializers(serializers.ModelSerializer):
    employee = UserProfileSerializers()

    class Meta:
        model = Personal
        fields = ['employee', 'post', 'marital_status', 'health_history', 'education',
                  'emergency_contacts', 'passport_number']

    def update(self, instance, validated_data):
        employee_data = validated_data.pop('employee', None)
        if employee_data:
            employee = instance.employee
            for attr, value in employee_data.items():
                setattr(employee, attr, value)
            employee.save()
        return super().update(instance, validated_data)


class VisitHistoryCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitHistoryComment
        fields = ['id', 'user', 'comment', 'visit']


class VisitHistoryCommentListSerializers(serializers.ModelSerializer):
    class Meta:
        model = VisitHistoryComment
        fields = ['comment']


class VisitHistoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitHistory
        fields = ['id', 'status', 'date', 'start_time', 'end_time', 'personal_status']


class VisitHistoryListSerializer(serializers.ModelSerializer):
    comment = VisitHistoryCommentListSerializers(read_only=True, many=True)

    class Meta:
        model = VisitHistory
        fields = ['id', 'status', 'date', 'start_time', 'end_time', 'comment', 'personal_status']


class StatusVacationRequestSerializers(serializers.ModelSerializer):
    class Meta:
        model = VacationRequest
        fields = ['status', 'start_date', 'end_date']


class PanelSerializers(serializers.ModelSerializer):
    personal_status = VisitHistoryListSerializer(many=True)
    employee = UserProfileSimpleSerializers()
    leave_status = StatusVacationRequestSerializers(read_only=True, many=True)

    class Meta:
        model = Personal
        fields = ['id', 'employee', 'personal_status', 'leave_status']


class StickerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sticker
        fields = ['id', 'image']


class AwardCreateSerializer(serializers.ModelSerializer): # Наградить сотрудника
    sticker = StickerSerializer(read_only=True)
    sticker_id = serializers.PrimaryKeyRelatedField(queryset=Sticker.objects.all(),  write_only=True, source='sticker')

    class Meta:
        model = Award
        fields = ['id', 'manager', 'employee', 'sticker', 'sticker_id']


class StickerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Sticker
        fields = ['image']


class AwardListSerializer(serializers.ModelSerializer):# Список награды для сотрудника
    sticker = StickerSerializers(read_only=True)

    class Meta:
        model = Award
        fields = ['id', 'sticker']


class VacationRequestCreateSerializers(serializers.ModelSerializer): # Форма заявки на отпуск
    class Meta:
        model = VacationRequest
        fields = ['id', 'type', 'from_who', 'manager', 'start_date', 'end_date', 'reason', 'document']

    def create(self, validated_data):
        validated_data['status'] = 'waiting'
        return super().create(validated_data)


class VacationRequestListSerializers(serializers.ModelSerializer): # Форма заявки на отпуск
    class Meta:
        model = VacationRequest
        fields = ['id', 'type', 'created_date', 'start_date', 'status', 'end_date', 'reason', 'document']


