from django.core.files import File
from django.shortcuts import get_object_or_404
from linksight.api.models import Dataset
from linksight.api.serializers import (DatasetPreviewSerializer,
                                       DatasetSerializer)
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from linksight.api.psgc_code_matcher import PSGCCodeMatcher

import pandas as pd


@api_view(['POST'])
@parser_classes((MultiPartParser,))
def dataset_list(request):
    if request.method == 'POST':
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
def dataset_process(request, id):
    psgc = get_object_or_404(Dataset, name='psgc_reference_file.csv')
    with psgc.file.open() as f:
        psgc_df = pd.read_csv(f)

    dataset = get_object_or_404(Dataset, pk=id)
    with dataset.file.open() as f:
        dataset_df = pd.read_csv(f)

    output_file = open('temp.csv', 'wb+')
    code_matcher = PSGCCodeMatcher(psgc_df, dataset_df)
    code_matcher.get_matches(output_file)

    file = File(output_file)
    created = Dataset.objects.create(file=file)
    output_file.close()

    serializer = DatasetSerializer(created)
    return Response(serializer.data, status=201)
