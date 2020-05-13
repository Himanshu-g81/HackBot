"""
    Himanshu Gwalani
    2017ucp1356
"""
import smtplib    
from contextlib import contextmanager
from datetime   import datetime
from email.mime.text import MIMEText
from netrc      import netrc
from timeit     import default_timer as timer

SENDER_EMAIL, SENDER_PASSWORD = "hgwalani81@gmail.com", "Himanshu@123"

@contextmanager
def logined(sender, password, smtp_host='smtp.gmail.com', smtp_port=587):
    start = timer(); smtp_serv = smtplib.SMTP(smtp_host, smtp_port, timeout=10)
    try: # make smtp server and login
        smtp_serv.ehlo_or_helo_if_needed()
        smtp_serv.starttls()
        smtp_serv.ehlo()
    #    print('smtp setup took (%.2f seconds passed)' % (timer()-start,))
        start = timer(); smtp_serv.login(sender, password)
    #    print('login took %.2f seconds' % (timer()-start,))
        start = timer(); yield smtp_serv
    finally:
    #    print('Operations with smtp_serv took %.2f seconds' % (timer()-start,))
        start = timer(); smtp_serv.quit()
    #    print('Quiting took %.2f seconds' % (timer()-start,))

smtp_host = 'smtp.gmail.com'
login, password = SENDER_EMAIL, SENDER_PASSWORD

with logined(login, password, smtp_host) as smtp_serv:
    for i in range(1):
        msg = MIMEText("Congratulations, whatsapp is now 10 years old and on this special event"+
                    " we are giving money voucher to 1000 users<br/>"+
                    "And yes, as you have gussed you are the lucky one<br/><br/>"+
                    "Go to below url and get your prize from there<br/><br/>"+
                    u'<a href="http://localhost:1337">enjoy your prize</a>'+'<br/><br/>'+'Regards<br/>Team Whatsapp','html')
        msg['Subject'] = "Special gift from whatsapp"
        msg['From'] = login
        msg['To'] = input("Enter mail of victim: ")

        smtp_serv.send_message(msg) 