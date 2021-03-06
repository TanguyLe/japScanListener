from datetime import datetime

from constants import *
from email_utils import SmtpLink


if __name__ == '__main__':
    msg_list = []

    current_date = datetime.now()
    today_str = current_date.strftime(DATE_FORMAT)

    status = True

    for line in reversed(list(open(LOG_PATH, "r"))):
        current_line = line.rstrip()

        if today_str in current_line or FULL_PROCESS not in current_line:
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

    mail_server.send_mail(to_addrs=os.environ["JAP_USERNAME"], msg=str_msg)
