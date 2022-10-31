import requests
import time
from datetime import datetime
import schedule
from SMTPmail import send_mail2
accounts_url = "http://127.0.0.1:8000/api/accounts/"
customer_url = "http://127.0.0.1:8000/api/"
transaction_url = "http://127.0.0.1:8000/api/transactions/"


def send_transaction_mail():
    accounts_response = requests.get(accounts_url)
    print(accounts_response.json())

    acc_no_list = [[str(i["acc_no"]), str(i["account_customer"])] for i in accounts_response.json()]
    for i, cif_id in acc_no_list:
        transaction_list_url = transaction_url+i+"/"
        trans_response = requests.get(transaction_list_url)
        details_to_send = trans_response.json()["Models to return"]
        transaction_logs = ""
        for k, j in enumerate(details_to_send):
            if str(j["sender_id"]) == str(i):
                transaction_logs += "\n" + str(k+1) + f")  Rs.{j['amount_sent']} sent to Account No XXXXXXXX\
{str(j['receiver_id'])[8:]} using transaction id {j['transaction_id']} at {str(j['datetime'])[:10]}"
            if str(j["receiver_id"]) == str(i):
                transaction_logs += "\n" + str(k+1) + f")  Rs.{j['amount_sent']} received from Account No XXXXXXXX\
{str(j['sender_id'])[8:]} using transaction id {j['transaction_id']} at {str(j['datetime'])[:10]}"
        message = f"Transaction logs for Acc. No {i} is {transaction_logs}"

        # Get customer email_id
        customer_email_url = customer_url+cif_id+"/"
        cust_response = requests.get(customer_email_url)
        cust_email = cust_response.json()["email_id"]
        send_mail2("kavinnithilr@gmail.com", message)


# send_transaction_mail()
# schedule.every(24).hours.do(send_transaction_mail)
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)

day, month = datetime.now().strftime("%Y"), datetime.now().strftime("%m")
print(day, month)
