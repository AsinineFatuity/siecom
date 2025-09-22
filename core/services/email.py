import requests
import logging
from decouple import config
from typing import List


class EmailService:
    def __init__(
        self,
        recipients: List[str],
        html_body: str,
    ):
        self._recipients = recipients
        self._subject = "Order Confirmation - Siecom Stores"
        self._html_body = html_body
        self._zepto_auth_token = config("ZEPTO_AUTH_TOKEN", default="", cast=str)
        self._zepto_url = "https://api.zeptomail.com/v1.1/email"
        self._default_mail_from = config("EMAIL_HOST_USER", default="", cast=str)

    def send_emails(self):
        headers = {
            "Authorization": self._zepto_auth_token,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        payload = {
            "from": {"address": self._default_mail_from, "name": "Siecom Stores"},
            "to": [
                {"email_address": {"address": recipient}}
                for recipient in self._recipients
            ],
            "subject": self._subject,
            "htmlbody": self._html_body,
            "attachments": [],
            "track_opens": True,
            "track_clicks": True,
        }
        response = requests.post(self._zepto_url, headers=headers, json=payload)
        logging.info(
            f"{__name__}: Zepto response: status code{response.status_code}, text \n - {response.text}"
        )
        return response
