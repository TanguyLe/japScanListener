import smtplib
from email.mime.text import MIMEText
import os


class SmtpLink:
    @staticmethod
    def create_service(address="smtp.gmail.com", port=587,
                       username=os.environ["JAP_USERNAME"], password=os.environ["JAP_PASSWORD"]):
        server = smtplib.SMTP(address + ':' + str(port))
        server.ehlo()
        server.starttls()
        server.login(username, password)

        return SmtpLink(server)

    def __init__(self, server):
        self.server = server

    def send_mail(self, to_addrs, msg, from_addr=os.environ["JAP_USERNAME"]):
        if type(to_addrs) == "string":
            to_addrs = [to_addrs]

        self.server.sendmail(from_addr=from_addr, to_addrs=to_addrs, msg=msg)

    @classmethod
    def get_string_email(cls, msg, subject, origin, destination):
        msg = MIMEText(msg)
        msg['Subject'] = subject
        msg['From'] = origin
        msg['To'] = destination

        return msg.as_string()

    def close(self):
        self.server.quit()

    def __del__(self):
        try:
            self.server.quit()
        except:
            pass
