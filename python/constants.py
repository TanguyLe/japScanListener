import os

d = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SCRAPPING_TIMEOUT = 60*15

SCRAPPING_STARTS = "Scrapping starts."
SCRAPPING_COMPLETED = "Scrapping completed."
SCRAPPING_FAILED_TEXT = "Scrapping failed."
SCRAPPING_FAILED = SCRAPPING_FAILED_TEXT + ": {error}"
JAPSCAN_URL = "http://www.japscan.com/"
MANGAKAKALOT_URL = "http://mangakakalot.com/"

DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = DATE_FORMAT + " %H:%M:%S"
LOG_FILENAME = "japscanListener.log"
LOG_PATH = os.path.join(d, LOG_FILENAME)

FULL_PROCESS = "full_process"

HTTP_CONNECTION_POOL = "HTTPConnectionPool"

VF_REGEX = "(\d+) VF"
CHAPTER_NUMBER_REGEX = "(chapter|chapter Extra|Chapter|Chapter Extra|Chap|chap|capter) ([0-9]+)"
FR_TYPE = "(FR)"
US_TYPE = "(US)"
RAW_TYPE = "(RAW)"
SPOILER_TYPE = "(SPOILER)"
START_MSH = "The following chapters are ready: \n"

SUBJECT = "Some Chapters are ready for you to read!"
ORIGIN = "JapScan Alert Tool"
DESTINATION = "Me"

SENDING_EMAILS = "Sending email(s)."
