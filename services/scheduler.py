import schedule
import time
from ..messages.message_service import send_message
from ..config.wa_config import NOMER_1, NOMER_2, NOMER_3
from ..messages.createMessage import create_messages

def send_message_to_number(number):
    messages = create_messages()
    if number in messages:
        response = send_message(number, messages[number])
        print(f"AI Message sent to {number} at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        return response
    time.sleep(2)  # Add delay between AI requests

def start_scheduler():
    # Schedule for NOMER_1 (every 2 minutes)
    schedule.every(2).minutes.do(send_message_to_number, NOMER_1)
    
    # Schedule for NOMER_2 (every 5 minutes)
    schedule.every(5).minutes.do(send_message_to_number, NOMER_2)

    # Schedule for NOMER_2 (every 5 minutes)
    schedule.every(7).minutes.do(send_message_to_number, NOMER_3)
    
    while True:
        schedule.run_pending()
        time.sleep(1)