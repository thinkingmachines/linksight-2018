import pandas as pd

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from linksight.api.models import Dataset
from linksight.api.psgc_code_matcher import PSGCCodeMatcher
from linksight.api.serializers import (DatasetMatchSerializer,
                                       DatasetPreviewSerializer,
                                       DatasetSerializer)
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response


@api_view(['POST'])
@parser_classes((MultiPartParser,))
def dataset_list(request):
    serializer = DatasetSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
def dataset_preview(request, id):
    dataset = get_object_or_404(Dataset, pk=id)
    serializer = DatasetPreviewSerializer(dataset)
    return Response(serializer.data)


@api_view(['POST'])
@parser_classes((JSONParser,))
def dataset_match(request, id):
    serializer = DatasetMatchSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    psgc = get_object_or_404(Dataset, pk=settings.PSGC_DATASET_ID)
    with psgc.file.open() as f:
        psgc_df = pd.read_csv(f)

    dataset = get_object_or_404(Dataset, pk=id)
    with dataset.file.open() as f:
        dataset_df = pd.read_csv(f)

    code_matcher = PSGCCodeMatcher(
        psgc_df,
        dataset_df,
        barangay_col=serializer.data['barangay_col'],
        city_municipality_col=serializer.data['city_municipality_col'],
        province_col=serializer.data['province_col'],
    )
    matches = code_matcher.get_matches(max_near_matches=3)

    return HttpResponse(matches.to_csv(index=False),
                        content_type='text/csv')
