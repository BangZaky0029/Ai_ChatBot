from datetime import datetime
from ..config.wa_config import NOMER_1, NOMER_2, NOMER_3
from ..core.order_analyzer import OrderAnalyzer
from ..core.message_generator import MessageGenerator

def create_messages():
    """Main function to create all messages"""
    analyzer = OrderAnalyzer()
    message_gen = MessageGenerator(analyzer)
    
    # Generate pending summary once to reuse
    pending_summary = message_gen.generate_pending_summary()
    
    messages = {
        # Admin Lilis with pending summary
        NOMER_1: f"{pending_summary.generate_admin_message(1001)}",
        # Admin Ina with pending summary
        NOMER_2: f"{pending_summary.generate_admin_message(1002)}",
        # Product message with pending summary
        NOMER_3: f"{pending_summary.generate_admin_message(1003)}"
    }
    
    return messages if any(messages.values()) else None