from rest_framework import serializers

from SMSApp.models import Customer, Accounts, TransactionHistory


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ("cif_id", "first_name", "last_name", "phone_number", "email_id")


class AccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = "__all__"


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionHistory
        fields = "__all__"
