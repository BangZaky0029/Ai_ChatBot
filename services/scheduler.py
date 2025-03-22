import schedule
import time
from ..config.wa_config import NOMER_1, NOMER_2, NOMER_3
from ..core.message_generator import MessageGenerator
from ..messages.message_service import send_whatsapp_message

def send_daily_messages():
    """Send daily messages to all admins"""
    msg_gen = MessageGenerator()
    
    # Admin specific messages
    admin_messages = {
        NOMER_1: msg_gen.generate_message(1001),  # Lilis
        NOMER_2: msg_gen.generate_message(1002),  # Ina
        NOMER_3: msg_gen.generate_message(1003)   # Indy
    }

    for phone, message in admin_messages.items():
        if send_whatsapp_message(phone, message):
            print(f"Message sent to {phone}")
        else:
            print(f"Failed to send message to {phone}")
        time.sleep(2)  # Delay between messages

def start_scheduler():
    """Start the message scheduler"""
    schedule.every().day.at("09:00").do(send_daily_messages)
    
    while True:
        schedule.run_pending()
        time.sleep(60)