from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProfileViewSet, SkillViewSet, LanguageViewSet, ExperienceViewSet,
    CourseViewSet, CertificateViewSet, DegreeViewSet, ProjectViewSet
)

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet)
router.register(r'skills', SkillViewSet)
router.register(r'languages', LanguageViewSet)
router.register(r'experiences', ExperienceViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'certificates', CertificateViewSet)
router.register(r'degrees', DegreeViewSet)
router.register(r'projects', ProjectViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
