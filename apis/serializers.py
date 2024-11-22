# debts/serializers.py
from rest_framework import serializers
from qarz.models import Debt, ReturnDebt

class ReturnDebtSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReturnDebt
        fields = ['id', 'amount', 'date']

class DebtSerializer(serializers.ModelSerializer):
    payments = ReturnDebtSerializer(many=True, read_only=True) 

    class Meta:
        model = Debt
        fields = ['id', 'customer_name', 'amount', 'description', 'is_active', 'duration_date', 'payments']

