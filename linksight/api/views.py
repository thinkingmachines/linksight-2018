from django.shortcuts import get_object_or_404
from drf_link_header_pagination import LinkHeaderPagination
from linksight.api.models import Dataset, Match
from linksight.api.serializers import (DatasetMatchSerializer,
                                       DatasetPreviewSerializer,
                                       DatasetSerializer, MatchItemSerializer,
                                       MatchSaveChoicesSerializer)
from rest_framework.decorators import (api_view, parser_classes,
                                       renderer_classes)
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework_csv.renderers import PaginatedCSVRenderer


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
    if serializer.is_valid():
        dataset = get_object_or_404(Dataset, pk=id)
        serializer.save(dataset=dataset)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
@renderer_classes((PaginatedCSVRenderer,))
def match_items(request, id):
    match = get_object_or_404(Match, pk=id)
    paginator = LinkHeaderPagination()
    page = paginator.paginate_queryset(match.items.all(), request)
    serializer = MatchItemSerializer(page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['POST'])
@parser_classes((JSONParser,))
def match_save_choices(request, id):
    serializer = MatchSaveChoicesSerializer(data=request.data)
    if serializer.is_valid():
        match = get_object_or_404(Match, pk=id)
        serializer.save(match=match)
        return Response(serializer.data, status=200)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
def match_preview(request, id):
    match = get_object_or_404(Match, pk=id)
    serializer = DatasetPreviewSerializer(match.matched_dataset)
    return Response(serializer.data)

