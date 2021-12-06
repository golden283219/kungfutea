from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http.response import JsonResponse
import json

from .models import MenuLink, QuickLink
from .serializers import MenuLinkSerializer, QuickLinkSerializer
from users.models import User


class MenuLinkViewSet(viewsets.ModelViewSet):
    serializer_class = MenuLinkSerializer
    queryset = MenuLink.objects.all()
    
    @action(detail=False, methods=['get'])
    def listWithRCInfo(self, request, *args, **kwargs):
        jsonData = self.get_serializer(MenuLink.objects.all(), many=True, context={'request': request}).data
        
        # Getting email in string from the reqeust Data.
        request_body_email = request.query_params.get("email")
        
        if request_body_email is not None:
            # Getting the RC password that password is request_email in Table User.
            user_email = User.objects.get(email=request_body_email)
            
            RC_user = user_email.RC_username
            RC_pwd = user_email.RC_password
            
            json_response = {'Links' : jsonData, 'RC_user' : RC_user, 'RC_pwd' : RC_pwd}

        else:
            json_response = {'Links' : jsonData}
                
        return JsonResponse(json_response, safe=False)


class QuickLinkViewSet(viewsets.ModelViewSet):
    serializer_class = QuickLinkSerializer
    queryset = QuickLink.objects.all()
    
    @action(detail=False, methods=['get'])
    def listWithRCInfo(self, request, *args, **kwargs):
        jsonData = self.get_serializer(QuickLink.objects.all(), many=True, context={'request': request}).data
        
        # Getting email in string from the reqeust Data.
        request_body_email = request.query_params.get("email")
        
        if request_body_email is not None:
            # Getting the RC password that password is request_email in Table User.
            user_email = User.objects.get(email=request_body_email)
            
            RC_user = user_email.RC_username
            RC_pwd = user_email.RC_password
            
            json_response = {'Links' : jsonData, 'RC_user' : RC_user, 'RC_pwd' : RC_pwd}

        else:
            json_response = {'Links' : jsonData}
                
        return JsonResponse(json_response, safe=False)
