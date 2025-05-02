from django.contrib import admin
from .models import Profile, Skill, Language, Experience, Course, Certificate, Degree, Project

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'linkedin', 'github', 'website')
    search_fields = ('user__username', 'linkedin', 'github', 'website')

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('profile', 'name', 'proficiency')
    search_fields = ('profile__user__username', 'name')

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('profile', 'name', 'level')
    search_fields = ('profile__user__username', 'name')

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('profile', 'company', 'title', 'start_date', 'end_date')
    search_fields = ('profile__user__username', 'company', 'title')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('profile', 'title', 'institution', 'completion_date')
    search_fields = ('profile__user__username', 'title', 'institution')

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('profile', 'name', 'issuer', 'issue_date')
    search_fields = ('profile__user__username', 'name', 'issuer')

@admin.register(Degree)
class DegreeAdmin(admin.ModelAdmin):
    list_display = ('profile', 'title', 'institution', 'completion_date')
    search_fields = ('profile__user__username', 'title', 'institution')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('profile', 'title', 'project_url')
    search_fields = ('profile__user__username', 'title')
