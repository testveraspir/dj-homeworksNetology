from rest_framework import serializers
from django.conf import settings
from rest_framework.exceptions import ValidationError

from students.models import Course


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "students")

    def validate_students(self, value):
        max_students = settings.MAX_STUDENTS_PER_COURSE
        if len(value) > max_students:
            raise ValidationError(f"Курс не может содержать больше {max_students} студентов.")
        return value
