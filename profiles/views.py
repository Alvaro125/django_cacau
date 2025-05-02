from rest_framework import viewsets, permissions
from rest_framework.response import Response

from .models import Profile, Skill, Language, Experience, Course, Certificate, Degree, Project
from .serializers import (
    ProfileSerializer, SkillSerializer, LanguageSerializer, ExperienceSerializer,
    CourseSerializer, CertificateSerializer, DegreeSerializer, ProjectSerializer
)

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    def list(self, request):
        queryset = self.get_queryset()

        if not queryset.exists():
            return Response({"detail": "Profile not found"}, status=404)

        profile = queryset.first()
        serializer = self.get_serializer(profile)
        return Response(serializer.data)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter skills to only those belonging to the user's profile
        try:
            profile = Profile.objects.get(user=self.request.user)
            return Skill.objects.filter(profile=profile)
        except Profile.DoesNotExist:
            # Return empty queryset if user has no profile
            return Skill.objects.none()

    def create(self, request):
        # Get the profile of the current user
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return Response({"error": "User profile not found"}, status=404)

        # Add the profile ID to the request data
        data = request.data.copy()
        data['profile'] = profile.id

        # Create the serializer with the modified data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

    def update(self, request, *args, **kwargs):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return Response({"error": "User profile not found"}, status=404)

        # Get the instance being updated
        instance = self.get_object()

        # Verify that the skill belongs to the user's profile
        if instance.profile.id != profile.id:
            return Response({"error": "Not authorized to update this skill"}, status=403)

        # Add the profile ID to the request data
        data = request.data.copy()
        data['profile'] = profile.id

        # Update the serializer with the modified data
        serializer = self.get_serializer(instance, data=data, partial=kwargs.get('partial', False))
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        try:
            profile = Profile.objects.get(user=self.request.user)
            return Language.objects.filter(profile=profile)
        except Profile.DoesNotExist:
            return Language.objects.none()

    def create(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return Response({"error": "User profile not found"}, status=404)

        data = request.data.copy()
        data['profile'] = profile.id

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

    def update(self, request, *args, **kwargs):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return Response({"error": "User profile not found"}, status=404)

        instance = self.get_object()

        if instance.profile.id != profile.id:
            return Response({"error": "Not authorized to update this experience"}, status=403)

        data = request.data.copy()
        data['profile'] = profile.id

        serializer = self.get_serializer(instance, data=data, partial=kwargs.get('partial', False))
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class ExperienceViewSet(viewsets.ModelViewSet):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter skills to only those belonging to the user's profile
        try:
            profile = Profile.objects.get(user=self.request.user)
            return Experience.objects.filter(profile=profile)
        except Profile.DoesNotExist:
            # Return empty queryset if user has no profile
            return Experience.objects.none()

    def create(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return Response({"error": "User profile not found"}, status=404)

        data = request.data.copy()
        data['profile'] = profile.id

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

    def update(self, request, *args, **kwargs):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return Response({"error": "User profile not found"}, status=404)

        instance = self.get_object()

        if instance.profile.id != profile.id:
            return Response({"error": "Not authorized to update this experience"}, status=403)

        data = request.data.copy()
        data['profile'] = profile.id

        serializer = self.get_serializer(instance, data=data, partial=kwargs.get('partial', False))
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        try:
            profile = Profile.objects.get(user=self.request.user)
            return Course.objects.filter(profile=profile)
        except Profile.DoesNotExist:
            return Course.objects.none()

    def create(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return Response({"error": "User profile not found"}, status=404)

        data = request.data.copy()
        data['profile'] = profile.id

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

    def update(self, request, *args, **kwargs):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return Response({"error": "User profile not found"}, status=404)

        instance = self.get_object()

        if instance.profile.id != profile.id:
            return Response({"error": "Not authorized to update this experience"}, status=403)

        data = request.data.copy()
        data['profile'] = profile.id

        serializer = self.get_serializer(instance, data=data, partial=kwargs.get('partial', False))
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class CertificateViewSet(viewsets.ModelViewSet):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        try:
            profile = Profile.objects.get(user=self.request.user)
            return Certificate.objects.filter(profile=profile)
        except Profile.DoesNotExist:
            return Certificate.objects.none()

    def create(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return Response({"error": "User profile not found"}, status=404)

        data = request.data.copy()
        data['profile'] = profile.id

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

    def update(self, request, *args, **kwargs):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return Response({"error": "User profile not found"}, status=404)

        instance = self.get_object()

        if instance.profile.id != profile.id:
            return Response({"error": "Not authorized to update this experience"}, status=403)

        data = request.data.copy()
        data['profile'] = profile.id

        serializer = self.get_serializer(instance, data=data, partial=kwargs.get('partial', False))
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class DegreeViewSet(viewsets.ModelViewSet):
    queryset = Degree.objects.all()
    serializer_class = DegreeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        try:
            profile = Profile.objects.get(user=self.request.user)
            return Degree.objects.filter(profile=profile)
        except Profile.DoesNotExist:
            return Degree.objects.none()

    def create(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return Response({"error": "User profile not found"}, status=404)

        data = request.data.copy()
        data['profile'] = profile.id

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

    def update(self, request, *args, **kwargs):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return Response({"error": "User profile not found"}, status=404)

        instance = self.get_object()

        if instance.profile.id != profile.id:
            return Response({"error": "Not authorized to update this experience"}, status=403)

        data = request.data.copy()
        data['profile'] = profile.id

        serializer = self.get_serializer(instance, data=data, partial=kwargs.get('partial', False))
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        try:
            profile = Profile.objects.get(user=self.request.user)
            return Project.objects.filter(profile=profile)
        except Profile.DoesNotExist:
            return Project.objects.none()

    def create(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return Response({"error": "User profile not found"}, status=404)

        data = request.data.copy()
        data['profile'] = profile.id

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

    def update(self, request, *args, **kwargs):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return Response({"error": "User profile not found"}, status=404)

        instance = self.get_object()

        if instance.profile.id != profile.id:
            return Response({"error": "Not authorized to update this experience"}, status=403)

        data = request.data.copy()
        data['profile'] = profile.id

        serializer = self.get_serializer(instance, data=data, partial=kwargs.get('partial', False))
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

