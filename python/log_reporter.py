from datetime import datetime, timedelta
import os

from constants import *
from email_utils import SmtpLink

from private_config import ME

if __name__ == '__main__':
    msg_list = []

    current_date = datetime.now()
    yesterday = current_date - timedelta(1)
    yesterday_str = yesterday.strftime(DATE_FORMAT)

    status = True
    d = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    for line in reversed(list(open(os.path.join(d, LOG_FILENAME), "r"))):
        current_line = line.rstrip()

        if yesterday_str not in current_line:
            if SCRAPPING_FAILED_TEXT in current_line and HTTP_CONNECTION_POOL not in current_line:
                status = False
            msg_list.append(current_line)
        else:
            break

    status_str = "OK" if status else "Error"

    mail_server = SmtpLink.create_service()

    str_msg = SmtpLink.get_string_email(msg="\n".join(msg_list),
                                        subject="JapScanListener Activity Report: " + status_str,
                                        origin=ORIGIN,
                                        destination=DESTINATION)

    mail_server.send_mail(to_addrs=ME, msg=str_msg)
