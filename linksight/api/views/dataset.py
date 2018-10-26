from django.shortcuts import get_object_or_404
from linksight.api.models import Dataset
from linksight.api.serializers import (DatasetMatchSerializer,
                                       DatasetPreviewSerializer,
                                       DatasetSerializer)
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response


@api_view(['POST'])
@parser_classes((MultiPartParser,))
def dataset_list(request):
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
def dataset_match(request, id):
    serializer = DatasetMatchSerializer(data=request.data)
    if serializer.is_valid():
        dataset = get_object_or_404(Dataset, pk=id)
        serializer.save(dataset=dataset)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

