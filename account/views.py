from ast import Expression
from multiprocessing import context
from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from account.serializers import LoginSerializer, LogoutUserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
# Create your views here.

class LoginUserView(GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request):
        serializer =  self.serializer_class(data = request.data, context = {'request': request})
        serializer.is_valid(raise_exception = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

class LogoutApiView(GenericAPIView):
    serializer_class = LogoutUserSerializer
    permission_classes  =  [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(status = status.HTTP_204_NO_CONTENT)
 