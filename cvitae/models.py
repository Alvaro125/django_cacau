from django.db import models
from accounts.models import CustomUser

class CVitae(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='cvitaes')
    url = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    def __str__(self):
        return f"Profile of {self.user.username}"