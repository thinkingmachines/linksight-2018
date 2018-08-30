import csv
from io import TextIOWrapper

from django.shortcuts import get_object_or_404
from linksight.api.models import Dataset
from linksight.api.serializers import (DatasetMatchSerializer,
                                       DatasetPreviewSerializer,
                                       DatasetSerializer)
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response
from silk.profiling.profiler import silk_profile


@api_view(['POST'])
@parser_classes((MultiPartParser,))
def dataset_list(request):
    try:
        file = request.data['file']
        csv_data = TextIOWrapper(file)
        row_count = sum(1 for row in csv.DictReader(csv_data))
        if row_count > 3000:
            return Response('too many rows', status=400)
    except Exception as exc:
        print(exc)
        return Response('invalid csv', status=400)

    context = {'uploader': request.user}
    serializer = DatasetSerializer(data=request.data, context=context)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
def dataset_preview(request, id):
    dataset = get_object_or_404(Dataset, pk=id)
    context = {'rows_shown': request.query_params.get('rowsShown', 10)}
    serializer = DatasetPreviewSerializer(dataset, context=context)
    return Response(serializer.data)


@api_view(['POST'])
@parser_classes((JSONParser,))
@silk_profile(name='Match dataset')
def dataset_match(request, id):
    serializer = DatasetMatchSerializer(data=request.data)
    if serializer.is_valid():
        dataset = get_object_or_404(Dataset, pk=id)
        serializer.save(dataset=dataset)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

