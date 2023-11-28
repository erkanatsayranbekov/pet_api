from djoser.serializers import UserCreatePasswordRetypeSerializer, UserCreateMixin
from .models import Teacher, UserAccount
from django.db import transaction
from rest_framework import serializers
from djoser.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationSerializer(UserCreatePasswordRetypeSerializer):
    __extra_data = {}

    def __init__(self, *args, **kwargs):
        self.__extra_data = kwargs.get('data')
        super().__init__(*args, **kwargs)
        self.fields["re_password"] = serializers.CharField(
            style={"input_type": "password"}
        )

    def create(self, validated_data):
        user = self.perform_create(validated_data)
        if user.is_teacher is True:
                    teacher_data = self.__extra_data.pop('teacher')
                    teacher = Teacher.objects.create(
                        experience=teacher_data['experience'], user=user)
                    teacher.save()
        else:
            user.is_student = True
            user.save()
        if settings.SEND_ACTIVATION_EMAIL:
            user.is_active = False
            user.save(update_fields=["is_active"])
        return user

            
    