import requests
from datetime import datetime
from ..config.wa_config import API_KEY, NOMER_1, NOMER_2, NOMER_3
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
    try:
        messages = create_messages()
        
        if not messages:
            raise Exception("Failed to generate AI messages")
        
        for number, message in messages.items():
            response = send_message(number, message)
            
            # Determine recipient type based on number
            if number == NOMER_1:
                recipient_type = "admin"
            elif number == NOMER_2:
                recipient_type = "user"
            elif number == NOMER_3:
                recipient_type = "admin_rizki"
            else:
                recipient_type = "unknown"
                
            print(f"AI Message sent to {recipient_type} ({number}) at {current_time}. Response: {response}")
        return response
    except Exception as e:
        print(f"Error in message service: {str(e)}")
        raise e