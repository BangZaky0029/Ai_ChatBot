import requests
from datetime import datetime
from ..config.wa_config import API_KEY, NOMER_1, NOMER_2
from .createMessage import create_messages

def send_message(phone, message):
    url = "https://api.fonnte.com/send"
    headers = {
        "Authorization": API_KEY
    }
    data = {
        "target": phone,
        "message": message
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

def send_scheduled_message():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    messages = create_messages()
    
    try:
        for number, message in messages.items():
            response = send_message(number, message)
            recipient_type = "admin" if number == NOMER_1 else "user"
            print(f"Message sent to {recipient_type} ({number}) at {current_time}. Response: {response}")
        return response
    except Exception as e:
        print(f"Error sending message: {str(e)}")
        raise e