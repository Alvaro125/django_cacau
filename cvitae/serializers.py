from rest_framework import serializers
from .models import CVitae

class CVitaeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CVitae
        fields = '__all__'