# utils/sms_utils.py
import nexmo
from django.conf import settings

def send_sms(to_phone_number, message):
    """
    Function to send SMS via Nexmo API.
    :param to_phone_number: Recipient's phone number (e.g., "+1234567890")
    :param message: The message to send
    :return: Response from Nexmo API
    """
    client = nexmo.Client(key=settings.NEXMO_API_KEY, secret=settings.NEXMO_API_SECRET)

    # Send the SMS
    response = client.send_message({
        'from': settings.NEXMO_VIRTUAL_NUMBER,
        'to': to_phone_number,
        'text': message,
    })

    if response["messages"][0]["status"] == "0":
        print(f"Message sent to {to_phone_number}")
        return True
    else:
        print(f"Failed to send message to {to_phone_number}. Error: {response['messages'][0]['error-text']}")
        return False
