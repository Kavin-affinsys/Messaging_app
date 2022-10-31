from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from datetime import datetime
# Create your views here.
from rest_framework import generics

from SMSApp.models import Customer, Accounts, TransactionHistory
from .serializers import CustomerSerializer, AccountsSerializer, TransactionSerializer


class CustomerAPIView(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class DetailsView(generics.RetrieveAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class AccountsView(generics.ListAPIView):
    queryset = Accounts.objects.all()
    serializer_class = AccountsSerializer


class AccountDetailsView(generics.RetrieveAPIView):
    # def get(self, request, acc_no):
    #     try:
    #         model = Accounts.objects.get(acc_no=acc_no)
    #     except Accounts.DoesNotExist:
    #         return Response(f"Account with {acc_no} is not Found", status=status.HTTP_404_NOT_FOUND)
    #     queryset = Accounts.objects.all()
    queryset = Accounts.objects.all()
    serializer_class = AccountsSerializer

    # return Response(serializer_class.data)

    def put(self, request, pk):
        try:
            model = Accounts.objects.get(acc_no=pk)
        except Accounts.DoesNotExist:
            return Response(f"Account with {pk} is not Found", status=status.HTTP_404_NOT_FOUND)
        serializer_class = AccountsSerializer(model, data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionsView(generics.ListAPIView):
    queryset = TransactionHistory.objects.all()
    serializer_class = TransactionSerializer

    def put(self, request, *args, **kwargs):
        try:
            pk = self.kwargs.get('pk')
            model = TransactionHistory.objects.get(transaction_id=pk)
        except TransactionHistory.DoesNotExist:
            return Response(f"Account with {pk} is not Found", status=status.HTTP_404_NOT_FOUND)
        serializer_class = AccountsSerializer(model, data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer_class = TransactionSerializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionDetailsView(generics.RetrieveAPIView):
    # queryset = TransactionHistory.objects.filter()
    # serializer_class = AccountsSerializer

    def get(self, request, *args, **kwargs):
        try:
            transaction_id = self.kwargs.get('transaction_id')
            # year, month = datetime.now().strftime("%Y"), datetime.now().strftime("%m")
            # model = TransactionHistory.objects.filter(sender_id=transaction_id) \
            #     .filter(datatime__year=f"{year}", datetime__month=f"{month}").values()
            model = TransactionHistory.objects.filter(sender_id=transaction_id).values()
            model1 = TransactionHistory.objects.filter(receiver_id=transaction_id).values()
            model = model | model1
            # model = model.order_by(transaction_id)
        except TransactionHistory.DoesNotExist:
            return Response(f"Account with {transaction_id} is not Found", status=status.HTTP_404_NOT_FOUND)
        return JsonResponse({"Models to return": list(model)})
