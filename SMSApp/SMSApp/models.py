from django.db import models


class Customer(models.Model):
    cif_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30, default="",)
    last_name = models.CharField(max_length=30, default="",)
    phone_number = models.IntegerField()
    email_id = models.EmailField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Accounts(models.Model):
    acc_no = models.IntegerField(primary_key=True)
    balance = models.IntegerField()
    bank_name = models.CharField(max_length=20, default="",)
    ifsc_code = models.CharField(max_length=12, default="",)
    account_customer = models.ForeignKey(Customer, related_name="Customer", on_delete=models.CASCADE)

    def __str__(self):
        return f"xxxxxxxx{str(self.acc_no)[8:]}"


class TransactionHistory(models.Model):
    sender = models.ForeignKey(Accounts, related_name="Sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(Accounts, related_name="receiver", on_delete=models.CASCADE)
    transaction_id = models.AutoField(primary_key=True,)
    amount_sent = models.IntegerField()
    datetime = models.DateTimeField()

    def __str__(self):
        return f"{self.sender} to {self.receiver}"
