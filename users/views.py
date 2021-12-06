from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .serializers import SignUpSerializer, UserSerializer, ChangePasswordSerializer, TokenObtainSerializer
from django.contrib.auth.hashers import make_password

from .models import User
from rest_framework.views import APIView

import json
import re
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework import status

from links.models import MenuLink
import codecs

from rest_framework import mixins, viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

User = get_user_model()


class UserViewSet(
    mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    http_method_names = ("post", "put", "patch")
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == "create":
            return SignUpSerializer
        elif self.action == "change_password":
            return ChangePasswordSerializer
        return UserSerializer

    def change_password(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response()

class links_and_RCPassword(APIView):
    def post(self, request):
        # SOP and POS link in dictionary data type
        label = MenuLink.objects.values_list("Label", flat=True)
        link = MenuLink.objects.values_list("Link", flat=True)
        
        label_link_list = []
        
        for label_index, link_index in zip(label, link):
            label_link_dict = {}
            label_link_dict["label"] = label_index
            label_link_dict["link"] = link_index
        
            label_link_list.append(label_link_dict)
        
        # Getting email in string from the reqeust Data.
        request_body_email = request.POST.get("email")
        
        if request_body_email is not None:
            # Getting the RC password that password is request_email in Table User.
            user_email = User.objects.get(email=request_body_email)
            
            RC_user = user_email.RC_username
            RC_pwd = user_email.RC_password
            
            json_response = {'Links' : label_link_list, 'RC_user' : RC_user, 'RC_pwd' : RC_pwd}

        else:
            json_response = {'Links' : label_link_list}
                
        return JsonResponse(json_response, safe=False)

class TokenObtainView(GenericAPIView):
    serializer_class = TokenObtainSerializer
    http_method_names = ("post",)
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token_set = Token.objects.filter(user=user)
        if token_set.exists():
            token_set.delete()
        token = Token.objects.create(user=user)

        return Response({"token": token.key}, status=status.HTTP_200_OK)
