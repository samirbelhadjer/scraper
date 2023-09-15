from rest_framework import generics
from .models import Ad
from rest_framework import serializers
from django.conf import settings


class AdsSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    class Meta:
        model = Ad
        fields = ['id', 'title', 'image_url', 'is_active', 'position']

    def validate_title(self,value):
        print('-------------->',value)
        return value

    def get_image_url(self, obj):
        base_url = settings.MEDIA_URL.replace('ads','banner')
        print('---->',base_url, "--->",obj.photo.name)
        return base_url + obj.photo.name

        

class AdsView(generics.ListAPIView):
    serializer_class = AdsSerializer
    queryset = Ad.objects.filter(is_active=True)
