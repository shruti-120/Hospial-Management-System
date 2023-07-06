from rest_framework.response import Response
from rest_framework.decorators import api_view
from app.models import *
from .serializers import *

@api_view(['GET'])
def getData(request):
    users = UserWithUserType.objects.all()
    serializer = UserWithUserTypeSerializers(users, many = True)
    return Response(serializer.data)

