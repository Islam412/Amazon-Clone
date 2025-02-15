from django.db.models.aggregates import Avg
from rest_framework import serializers
from taggit.serializers import TagListSerializerField , TaggitSerializer


from .models import Product , Brand , Review


class BrandListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'