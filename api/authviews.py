from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from api.authserializers import RegisterSerializer, CustomTokenObtainPairSerializer, CustomTokenRefreshSerializer

class RegisterView(generics.CreateAPIView):
    
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer_class()
        serializer = serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()

            response = Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
            
            response.delete_cookie(
                'refresh_token', 
                path='/auth/token/' 
            )
            return response
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            refresh_token = response.data.pop('refresh')  
            
            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,   
                secure=True,     
                samesite='Lax',  
                path='/auth/token/'  
            )
            
        return response
    
class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            mutable_data = request.data.copy()
            mutable_data['refresh'] = refresh_token
            request._full_data = mutable_data 

        return super().post(request, *args, **kwargs)