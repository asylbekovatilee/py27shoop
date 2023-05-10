
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404, redirect

from .serializers import RegisterUserSerializers
from .models import User

class RegisterUserView(APIView):
    @swagger_auto_schema(request_body=RegisterUserSerializers())
    def post(self, request):
        serializer = RegisterUserSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("вы успешно зарег", status=201)

class ActivateView(APIView):
    def get(self, request, activation_code):
        user = get_object_or_404(User, activation_code=activation_code)
        user.is_active = True
        user.activation_code = ''
        user.save()
        return redirect("https://google.com")