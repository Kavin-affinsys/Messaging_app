import requests
from datetime import datetime
from SMTPmail import send_mail2, send_sms

accounts_url = "http://127.0.0.1:8000/api/accounts/"
customer_url = "http://127.0.0.1:8000/api/"
transaction_url = "http://127.0.0.1:8000/api/transactions/"


def sender_debit(sender_endpoint, amount, sender, transaction_id, date_time, receiver):
    sender_response = requests.put(sender_endpoint,
                                   data={
                                       "acc_no": sender.json()["acc_no"],
                                       "balance": sender.json()["balance"] - amount,
                                       "bank_name": sender.json()["bank_name"],
                                       "ifsc_code": sender.json()["ifsc_code"],
                                       "account_customer": sender.json()["account_customer"],
                                   })
    sender_url_customer = f"{customer_url}{sender.json()['account_customer']}/"
    cust_response = requests.get(url=sender_url_customer)
    receiver_phone_number = requests.get(f"{customer_url}{receiver.json()['account_customer']}/").json()["phone_number"]

    message = f"Rs.{str(amount)} is debited from your Bank acc XXXXXXXX{str(sender.json()['acc_no'])[8:]} on \
{str(date_time)[:10]} at {str(date_time)[11:16]} by account linked to the mobile number \
XXXXXX{str(receiver_phone_number)[6:]}. The transaction id of the transaction is {str(transaction_id)}."

    send_mail2(cust_response.json()["email_id"], message)
    send_sms("+917358699130", message)
    print(sender_response.text)


def receiver_credit(receiver_endpoint, amount, receiver, transaction_id, date_time, sender):
    receiver_response = requests.put(receiver_endpoint,
                                     data={
                                         "acc_no": receiver.json()["acc_no"],
                                         "balance": receiver.json()["balance"] + amount,
                                         "bank_name": receiver.json()["bank_name"],
                                         "ifsc_code": receiver.json()["ifsc_code"],
                                         "account_customer": receiver.json()["account_customer"],
                                     })
    receiver_url_customer = f"{customer_url}{receiver.json()['account_customer']}/"
    cust_response = requests.get(url=receiver_url_customer)
    sender_phone_number = requests.get(f"{customer_url}{sender.json()['account_customer']}/").json()["phone_number"]

    message = f"Rs.{str(amount)} is credited to your Bank acc XXXXXXXX{str(receiver.json()['acc_no'])[8:]} on \
{str(date_time)[:10]} at {str(date_time)[11:16]} by account linked to the mobile number \
XXXXXX{str(sender_phone_number)[6:]}. The transaction id of the transaction is {str(transaction_id)}."

    send_mail2(cust_response.json()["email_id"], message)
    print(receiver_response.text)


def initiate_transactions(acc_no_sender, acc_no_receiver, transaction_amount):
    sender_endpoint = f'{accounts_url}{acc_no_sender}/'
    receiver_endpoint = f'{accounts_url}{acc_no_receiver}/'
    try:
        if acc_no_sender == acc_no_receiver:
            raise Exception("Can't transfer to same account")
        sender = requests.get(sender_endpoint)
        print(sender.json())
        balance_sender = sender.json()["balance"]
        print(balance_sender)
        if balance_sender < transaction_amount:
            raise Exception("The amount trying to send is more than the balance available")
        cif_sender = sender.json()["account_customer"]
        print(cif_sender)
        receiver = requests.get(receiver_endpoint)
        print(receiver.json())
        cif_receiver = receiver.json()["account_customer"]
        print(cif_receiver)
        transactions_update = requests.post(transaction_url, data={
            "sender": acc_no_sender,
            "receiver": acc_no_receiver,
            "amount_sent": transaction_amount,
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M"),
        })
        sender_debit(sender_endpoint, transaction_amount, sender, transactions_update.json()["transaction_id"],
                     transactions_update.json()["datetime"], receiver)
        receiver_credit(receiver_endpoint, transaction_amount, receiver, transactions_update.json()["transaction_id"],
                        transactions_update.json()["datetime"], sender)
        print(transactions_update.text)
    except Exception:
        print("Exception triggered !")


initiate_transactions(322312343214, 123123321312, 1000)
