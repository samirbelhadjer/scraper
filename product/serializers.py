from rest_framework import serializers, exceptions
from .models import Product, Categorie
from re import match
from django.conf import settings


class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = ['id', 'categorie_name', 'is_active']


class ProductSerializer(serializers.ModelSerializer):
    categorie = CategorieSerializer(many=True, read_only=True)
    image_url = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id', 'full_name', 'image_url', 'price', 'original_link', 'original_store', 'brand', 'staff_pick', 'description', 'categorie', 'time_added']

    def get_image_url(self, obj):
        return settings.MEDIA_URL + obj.photo.name

class ProductSeedingSerializer(serializers.Serializer):
    file = serializers.FileField(required=True, write_only=True, allow_empty_file=False,)
    original_store = serializers.CharField(max_length=255, allow_blank=False, required=True)
    categorie = serializers.CharField(max_length=255, allow_blank=False, required=True)

    def validate_file(self, file):
        if file.content_type != 'application/json':
            raise exceptions.ValidationError('Only json files accepted')
        return file


class BrandSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Product
        fields = ['brand', 'count']


class StoreSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Product
        fields = ['original_store', 'count']



class StoreSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Product
        fields = ['original_store', 'count']




class AddProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
