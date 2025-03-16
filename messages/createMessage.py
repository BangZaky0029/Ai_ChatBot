from datetime import datetime
from ..config.wa_config import NOMER_1, NOMER_2, NOMER_3
from .deepSeekAi import get_ai_response

def create_messages():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Generate AI responses for each recipient
    admin_prompt = "Generate a short professional reminder message for a design deadline"
    user_prompt = "Generate a casual friendly message asking about tomorrow's schedule"
    admin_rizki = "Generate a brief project update notification message"
    
    admin_message = get_ai_response(admin_prompt)
    user_message = get_ai_response(user_prompt)
    operator_message = get_ai_response(admin_rizki)
    
    return {
        NOMER_1: f"{admin_message}\n\nSent at: {current_time}",
        NOMER_2: f"{user_message}\n\nSent at: {current_time}",
        NOMER_3: f"{operator_message}\n\nSent at: {current_time}"
    }
