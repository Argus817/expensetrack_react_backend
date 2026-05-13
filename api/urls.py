from django.urls import path

from api.views import HelloView, CreateExpenseView, UserExpenseListView, UpdateExpenseView

urlpatterns = [
    path('hello/', HelloView.as_view(), name='hello'),
    path('expense/', UserExpenseListView.as_view(), name='get_expense'),
    path('expense/create/', CreateExpenseView.as_view(), name='add_expense'),
    path('expense/update/<int:pk>/', UpdateExpenseView.as_view(), name='update_expense'),
]