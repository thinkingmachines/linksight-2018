from django.core.exceptions import PermissionDenied
from linksight.api.serializers import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def user_detail(request, id):
    if id == 'me':
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    raise PermissionDenied()
