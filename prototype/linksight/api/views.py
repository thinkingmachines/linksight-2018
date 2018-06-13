from linksight.api.serializers import DatasetSerializer
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response


@api_view(['POST'])
@parser_classes((MultiPartParser,))
def dataset_list(request):
    if request.method == 'POST':
        serializer = DatasetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
