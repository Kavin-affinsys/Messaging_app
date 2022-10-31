import smtplib
from decouple import config
from twilio.rest import Client


def send_mail(to_email, type_of_trans, amount, account_no, date_time, from_phone_number, transaction_id):
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    # start TLS for security
    s.starttls()
    # Authentication
    s.login("kavin.nithil@affinsys.com", config("EMAIL_PASSWORD"))

    # message
    message = f"Your Bank acc XXXXXXXX{str(account_no)[8:]} is {type_of_trans}ed Rs.{str(amount)} on {date_time[:10]}\
 at {date_time[11:16]} by account linked to the mobile number XXXXXX{str(from_phone_number)[6:]}. The transaction id of\
 the transaction is {transaction_id}."
    print(message)

    # s.sendmail("kavin.nithil@affinsys.com", to_email, msg=message)
    print(f"Mail sent to {to_email}")
    s.quit()


def send_mail2(to_email, message):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    # start TLS for security
    s.starttls()
    # Authentication
    s.login("kavin.nithil@affinsys.com", config("EMAIL_PASSWORD"))
    print(message)
    # s.sendmail("kavin.nithil@affinsys.com", to_email, msg=message)
    print(f"Mail sent to {to_email}")
    s.quit()


def send_sms(to_number, message):
    account_sid = config("TWILIO_ACCOUNT_SID")
    auth_token = config('TWILIO_AUTH_TOKEN')
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
        body=message,
        from_='+13023053794',
        to='+917358699130'
    )

    print(message.sid)


# send_mail("xyz@gmail.com", "debit", 1000, "123412341234", "2022-10-30T14:15:00Z", 1234123412, 20)
# send_sms("1", "Hello Kavin, This is message from twilio")
