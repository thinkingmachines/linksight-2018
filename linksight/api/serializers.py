import os.path

from django.contrib.auth import get_user_model
from linksight.api.models import Dataset, Match, MatchItem
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name')


class DatasetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dataset
        fields = '__all__'

    def create(self, validated_data):
        name = os.path.basename(validated_data['file'].name)
        return super().create({'name': name, **validated_data})


class DatasetPreviewSerializer(serializers.BaseSerializer):

    def to_representation(self, obj):
        return obj.preview(n=self.context['rows_shown'])


class DatasetMatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Match
        fields = '__all__'
        read_only_fields = ('dataset',)

    def create(self, validated_data):
        obj = super().create(validated_data)
        obj.generate_match_items(**validated_data)
        return obj


class MatchItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = MatchItem
        exclude = ('match',)


class MatchSaveChoicesSerializer(serializers.BaseSerializer):

    match_choices = serializers.DictField(child=serializers.IntegerField())

    def to_internal_value(self, data):
        return data

    def to_representation(self, obj):
        match = obj.pop('match')
        return {
            'match': match.id,
            'matched_dataset': match.matched_dataset.id,
        }

    def create(self, validated_data):
        match_choices = validated_data['match_choices']
        match = validated_data['match']
        match.save_choices(match_choices)
        return validated_data

