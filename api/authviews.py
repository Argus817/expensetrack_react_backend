from rest_framework import generics
from rest_framework.response import Response

from api.serializers import RegisterSerializer

class RegisterView(generics.CreateAPIView):
    
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer_class()
        serializer = serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created'}, status=201)
        return Response(serializer.errors, status=400)