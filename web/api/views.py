from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  # <-- Here
from rest_framework.authtoken.models import Token
from login import models
from login.models import UserDetails as ud
import requests


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)             # <-- And here
    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


class Registration(APIView):
    def post(self, request):
        data = request.data
        print(data)
        user = models.UserDetails(username=data['name'], password=data['password'],
                                  phone=data['phone'], email=data['email'])
        user.save()
        print(user.email)
        token = Token.objects.create(user=user)
        return Response({'token': token.key})
        '''if data['user'] == 'Nikita' and data['pass'] == '112233':
            user = models.UserDetails(username=data['user'], password=data['pass'])
            user.save()
            token = Token.objects.create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid'})'''


class TokenGen(APIView):
    def post(self, request):
        data = request.data
        print("Data Decoded")
        user = models.UserDetails.objects.get(username=data['name'])
        print("Data Saved")
        token = Token.objects.get(user=user)
        return Response({'token': token.key})


class Verify(APIView):
    def post(self, request):
        data = request.data
        details = models.UserDetails.objects.filter(token=data['token']).exists()
        print(details)
        if details == True:
            return Response({'exists': 'true'})
        else:
            return Response({'exists': 'false'})






