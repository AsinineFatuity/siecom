import logging
import traceback
from typing import Any, Dict
import africastalking
from decouple import config


class SMSService:
    def __init__(self, recipients: list[str], message: str):
        self._recipients = recipients
        self._message = message
        self._sms_service = None
        self._at_api_key = config("AT_API_KEY")
        self._at_username = config("AT_USERNAME")
        self._init_service()
        self._format_phone_numbers()
        self._response = {"message": message, "recipients": []}

    def _init_service(self):
        try:
            africastalking.initialize(self._at_username, self._at_api_key)
            self._sms_service = africastalking.SMS
        except Exception as e:
            traceback.print_exc()
            logging.error(f"{__name__}: Failed to initialize SMS service: {e}")

    def _format_phone_numbers(self):
        for i, recipient in enumerate(self._recipients):
            if not recipient.startswith("+"):
                self._recipients[i] = f"+{recipient}"
            self._recipients[i] = self._recipients[i].replace(" ", "")

    def send_sms(self):
        if not self._sms_service:
            logging.error(f"{__name__}: SMS service not initialized.")
            return self._response
        try:
            response = self._sms_service.send(self._message, self._recipients)
            self._response = self._format_response(response)
        except Exception as e:
            traceback.print_exc()
            logging.error(f"{__name__}: Failed to send SMS: {e}")
        return self._response

    def _format_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        formatted_response = {
            "message": response.get("message", ""),
            "recipients": response.get("recipients", []),
        }
        return formatted_response
