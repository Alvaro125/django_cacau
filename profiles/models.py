# profiles/models.py

from django.db import models
from accounts.models import CustomUser

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"

class Skill(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)
    proficiency = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} ({self.proficiency})"

class Language(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='languages')
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} ({self.level})"

class Experience(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='experiences')
    company = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} at {self.company}"

class Course(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='courses')
    title = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    completion_date = models.DateField()

    def __str__(self):
        return f"{self.title} ({self.institution})"

class Certificate(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='certificates')
    name = models.CharField(max_length=255)
    issuer = models.CharField(max_length=255)
    issue_date = models.DateField()

    def __str__(self):
        return f"{self.name} issued by {self.issuer}"

class Degree(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='degrees')
    title = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    completion_date = models.DateField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} at {self.institution}"

class Project(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    project_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title
