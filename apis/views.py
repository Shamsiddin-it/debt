# debts/views_api.py
from rest_framework import generics, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from qarz.models import Debt, ReturnDebt
from .serializers import DebtSerializer, ReturnDebtSerializer
from django.urls import reverse_lazy

class DebtListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        debts = Debt.objects.all() 
        serializer = DebtSerializer(debts, many=True)
        total_debt = Debt.objects.aggregate(Sum('amount'))['amount__sum']
        total_debt = total_debt if total_debt else 0.00
        debtors = Debt.objects.filter(is_active=True).values('customer_name').distinct().count()

        data = {
            'debts': serializer.data,
            'total_debt': total_debt,
            'debtors': debtors
        }

        return Response(data, status=status.HTTP_200_OK)

class ActiveDebtListAPIView(generics.ListAPIView):
    queryset = Debt.objects.filter(is_active=True)
    serializer_class = DebtSerializer

class PaidDebtListAPIView(generics.ListAPIView):
    queryset = Debt.objects.filter(is_active=False)
    serializer_class = DebtSerializer

class DebtDetailAPIView(generics.RetrieveAPIView):
    queryset = Debt.objects.all()
    serializer_class = DebtSerializer
    lookup_field = 'pk'  

class DebtCreateAPIView(generics.CreateAPIView):
    queryset = Debt.objects.all()
    serializer_class = DebtSerializer

class ReturnDebtCreateAPIView(generics.CreateAPIView):
    serializer_class = ReturnDebtSerializer

    def perform_create(self, serializer):
        debt = get_object_or_404(Debt, pk=self.kwargs['pk'])
        return_debt = serializer.save(debt=debt)

        if return_debt.payback():
            return return_debt
        else:
            raise serializers.ValidationError("Payment amount exceeds the debt amount.")

    def get_success_url(self):
        return reverse_lazy('debt_detail', kwargs={'pk': self.kwargs['pk']})

class DebtPaymentsAPIView(APIView):
    def get(self, request, pk, *args, **kwargs):
        debt = get_object_or_404(Debt, pk=pk)
        payments = ReturnDebt.objects.filter(debt=debt)
        serializer = ReturnDebtSerializer(payments, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

