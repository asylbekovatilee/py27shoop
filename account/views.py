from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import RegisterUserSerializers

class RegisterUserView(APIView):
    def post(self, request):
        serializer = RegisterUserSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("вы успешно зарег", status=201)
