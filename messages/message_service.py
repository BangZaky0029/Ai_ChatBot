import requests
from datetime import datetime
from ..config.wa_config import API_KEY
from ..core.message_generator import MessageGenerator

def send_whatsapp_message(phone, message):
    """Send WhatsApp message using Fonnte API"""
    if not message:
        print(f"Empty message for {phone}")
        return False

    url = "https://api.fonnte.com/send"
    payload = {
        "target": phone,
        "message": message
    }
    headers = {
        "Authorization": API_KEY
    }

    try:
        response = requests.post(url, headers=headers, data=payload, timeout=30)
        if response.status_code != 200:
            print(f"Error sending message: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Failed to send message: {str(e)}")
        return False

def send_scheduled_message():
    """Send scheduled messages to all admins"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        messages = create_messages()
        
        if not messages:
            print(f"[{current_time}] No pending orders to report.")
            return
            
        # Send messages to each admin
        for phone, message in messages.items():
            if message and send_message(phone, message):
                print(f"[{current_time}] Message sent successfully to {phone}")
            else:
                print(f"[{current_time}] Failed to send message to {phone}")
                
    except Exception as e:
        print(f"[{current_time}] Error in send_scheduled_message: {e}")