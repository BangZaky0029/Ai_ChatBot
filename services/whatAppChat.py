from flask import Blueprint, jsonify
import threading
from .scheduler import start_scheduler
from ..messages.message_service import send_message
from ..config.wa_config import NOMER_1, NOMER_2, NOMER_3
from ..messages.createMessage import create_messages

# Create blueprint with correct name
whatsapp_bp = Blueprint('whatsapp', __name__)

@whatsapp_bp.route("/", methods=["GET"])
def home():
    return jsonify({"status": "success", "message": "Message Scheduler API is running!"})

@whatsapp_bp.route("/send-message", methods=["POST"])
def send_message_now():
    try:
        messages = create_messages()
        responses = {
            "NOMER_1": send_message(NOMER_1, messages[NOMER_1]),
            "NOMER_2": send_message(NOMER_2, messages[NOMER_2]),
            "NOMER_3": send_message(NOMER_3, messages[NOMER_3])
        }
        return jsonify({
            "status": "success", 
            "message": "Messages sent successfully!",
            "responses": responses
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@whatsapp_bp.route("/get-data", methods=["GET"])
def get_data():
    try:
        data = get_data_from_db()
        return jsonify({
            "status": "success",
            "data": data
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def init_scheduler():
    scheduler_thread = threading.Thread(target=start_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()
