import os.path

from linksight.api.models import Dataset
from rest_framework import serializers


class DatasetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dataset
        fields = '__all__'

    def create(self, validated_data):
        name = os.path.basename(validated_data['file'].name)
        return super().create(dict(name=name, **validated_data))


class DatasetPreviewSerializer(serializers.BaseSerializer):

    def to_representation(self, obj):
        return obj.preview()

