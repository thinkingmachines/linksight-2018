import os.path

import pandas as pd

from django.conf import settings
from linksight.api.models import Dataset, Match, MatchItem
from linksight.api.psgc_code_matcher import PSGCCodeMatcher
from rest_framework import serializers


class DatasetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dataset
        fields = '__all__'

    def create(self, validated_data):
        name = os.path.basename(validated_data['file'].name)
        return super().create({'name': name, **validated_data})


class DatasetPreviewSerializer(serializers.BaseSerializer):

    def to_representation(self, obj):
        return obj.preview()


class DatasetMatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Match
        fields = '__all__'
        read_only_fields = ('dataset',)

    def clean_matches(self, matches):
        for col in matches:
            if col.endswith('score'):
                filler = 0
            else:
                filler = None
            matches[col] = matches[col].where(pd.notnull(matches[col]),
                                              filler)
        return matches

    def create(self, validated_data):
        psgc = Dataset.objects.get(pk=settings.PSGC_DATASET_ID)
        with psgc.file.open() as f:
            psgc_df = pd.read_csv(f, dtype={'code': object})

        obj = super().create(validated_data)
        with obj.dataset.file.open() as f:
            dataset_df = pd.read_csv(f)

        matcher = PSGCCodeMatcher(
            psgc_df,
            dataset_df,
            barangay_col=validated_data['barangay_col'],
            city_municipality_col=validated_data['city_municipality_col'],
            province_col=validated_data['province_col'],
        )
        matches = matcher.get_matches(max_near_matches=3)
        matches = self.clean_matches(matches)

        for _, row in matches.iterrows():
            MatchItem.objects.create(match=obj, **row.to_dict())

        return obj


class MatchItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = MatchItem
        exclude = ('match',)


class MatchCheckSerializer(serializers.BaseSerializer):

    match_choices = serializers.DictField(child=serializers.IntegerField())

    def to_internal_value(self, data):
        return data

    def to_representation(self, obj):
        return {
            **obj,
            'match': obj['match'].id,
        }

    def create(self, validated_data):
        match_choices = validated_data['match_choices']
        match = validated_data['match']
        match.items.filter(
            id__in=match_choices.values(),
        ).update(chosen=True)
        return validated_data

