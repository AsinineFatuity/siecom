import logging
import traceback
from typing import Any, Dict
import africastalking
from decouple import config


class SMSService:
    AT_API_KEY = config("AT_API_KEY")
    AT_USERNAME = config("AT_USERNAME")

    def __init__(self, phone_number: str, message: str):
        self.phone_number = phone_number
        self.message = message
        self.sms_service = None
        self._init_service()
        self._format_phone_number()
        self._response = {"message": message, "recipients": []}

    def _init_service(self):
        try:
            africastalking.initialize(self.AT_USERNAME, self.AT_API_KEY)
            self.sms_service = africastalking.SMS
        except Exception as e:
            traceback.print_exc()
            logging.error(f"{__name__}: Failed to initialize SMS service: {e}")

    def _format_phone_number(self):
        if not self.phone_number.startswith("+"):
            self.phone_number = f"+{self.phone_number}"

    def send_sms(self):
        if not self.sms_service:
            logging.error(f"{__name__}: SMS service not initialized.")
            return self._response
        try:
            response = self.sms_service.send(self.message, [self.phone_number])
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
