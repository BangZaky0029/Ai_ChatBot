from datetime import datetime
from ..config.wa_config import NOMER_1, NOMER_2

def create_messages():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return {
        NOMER_1: f"IMAM, jangan lupa desain deadline tgl 18 yak!                                  \n\n\nnotification at: {current_time}",
        NOMER_2: f"LUKAS Besok kuliah gak?                          \n\n\nnotification at: {current_time}"
    }