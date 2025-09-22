class SMSService:
    SANDBOX_URL = "https://api.sandbox.africastalking.com/version1/messaging"

    def __init__(self, phone_number: str, message: str):
        self.phone_number = phone_number
        self.message = message

    def send_sms(self):
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }
