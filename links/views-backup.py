from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import SopAndPosLink
from .serializers import SopAndPosLinkSerializer

    
class SopAndPosLinkList(APIView):
    def post(self, request):
        links = SopAndPosLink.objects.all()
        serializer = SopAndPosLinkSerializer(links, many="true")
        return Response(serializer.data)