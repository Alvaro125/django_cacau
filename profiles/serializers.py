from rest_framework import serializers

from accounts.models import CustomUser
from .models import Profile, Skill, Language, Experience, Course, Certificate, Degree, Project

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = '__all__'

class DegreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Degree
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True, source='skill_set')
    languages = LanguageSerializer(many=True, read_only=True, source='language_set')
    experiences = ExperienceSerializer(many=True, read_only=True, source='experience_set')
    courses = CourseSerializer(many=True, read_only=True, source='course_set')
    certificates = CertificateSerializer(many=True, read_only=True, source='certificate_set')
    degrees = DegreeSerializer(many=True, read_only=True, source='degree_set')
    projects = ProjectSerializer(many=True, read_only=True, source='project_set')

    # user não é necessário no input do cliente
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Profile
        fields = [
            'id', 'user', 'linkedin', 'github', 'website', 'bio',
            'skills', 'languages', 'experiences', 'courses',
            'certificates', 'degrees', 'projects'
        ]

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('user', None)  # evita sobrescrever o user
        return super().update(instance, validated_data)


