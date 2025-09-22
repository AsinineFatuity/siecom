import requests
import logging
from decouple import config
from typing import List


class ZeptoMailClient:
    ZEPTO_AUTH_TOKEN = config("ZEPTO_AUTH_TOKEN", default="", cast=str)
    ZEPTO_URL = "https://api.zeptomail.com/v1.1/email"
    DEFAULT_MAIL_FROM = config("EMAIL_HOST_USER", default="", cast=str)

    def __init__(
        self,
        recipients: List[str],
        html_body: str,
    ):
        self.recipients = recipients
        self.subject = "Order Confirmation - Siecom Stores"
        self.html_body = html_body

    def send_emails(self):
        headers = {
            "Authorization": self.ZEPTO_AUTH_TOKEN,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        payload = {
            "from": {"address": self.DEFAULT_MAIL_FROM, "name": "Siecom Stores"},
            "to": [
                {"email_address": {"address": recipient}}
                for recipient in self.recipients
            ],
            "subject": self.subject,
            "htmlbody": self.html_body,
            "attachments": [],
            "track_opens": True,
            "track_clicks": True,
        }
        response = requests.post(self.ZEPTO_URL, headers=headers, json=payload)
        logging.info(
            f"{__name__}: Zepto response: status code{response.status_code}, text \n - {response.text}"
        )
        return response
