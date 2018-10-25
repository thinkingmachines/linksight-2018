from django.core.exceptions import PermissionDenied
from linksight.api.serializers import UserSerializer, TokenSerializer
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def user_detail(request, id):
    if id == 'me':
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    raise PermissionDenied()


@api_view(['POST'])
def user_tokens(request, id):
    if id == 'me':
        token, _ = Token.objects.get_or_create(user=request.user)
        serializer = TokenSerializer(token)
        return Response(serializer.data)
    raise PermissionDenied()
