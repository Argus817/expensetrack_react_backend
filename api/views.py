from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api.serializers import ExpenseSerializer
from api.models import Expense

# Create your views here.
class HelloView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        print(request.user)
        return Response({'message': 'hello'})
    
class CreateExpenseView(CreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UpdateExpenseView(RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

class UserExpenseListView(ListAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user).order_by('-timestamp')