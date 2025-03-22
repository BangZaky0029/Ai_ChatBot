from flask import Blueprint, jsonify, request
import threading
import time
from ..core.message_generator import MessageGenerator
from ..messages.message_service import send_whatsapp_message
from ..config.wa_config import NOMER_1, NOMER_2, NOMER_3
from ..messages.deepSeekAi import get_ai_response
from .scheduler import start_scheduler

whatsapp_bp = Blueprint('whatsapp', __name__)

@whatsapp_bp.route("/test-ai", methods=["POST"])
def test_ai():
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        
        msg_gen = MessageGenerator()
        summary = msg_gen.generate_summary()
        
        ai_prompt = f"""Analisis dan berikan ringkasan dari data berikut:

{summary}

Tolong berikan:
1. Total pesanan pending per deadline
2. Highlight pesanan urgent (jika ada)
3. Saran prioritas pengerjaan
"""
        ai_response = get_ai_response(ai_prompt)
        
        return jsonify({
            "status": "success",
            "prompt": prompt,
            "response": ai_response,
            "raw_summary": summary
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@whatsapp_bp.route("/send-messages", methods=["POST"])
def send_messages():
    try:
        msg_gen = MessageGenerator()
        results = {}
        
        # Send to each admin
        for phone, admin_id in [(NOMER_1, 1001), (NOMER_2, 1002), (NOMER_3, 1003)]:
            message = msg_gen.generate_message(admin_id)
            success = send_whatsapp_message(phone, message)
            results[phone] = "Success" if success else "Failed"
            time.sleep(2)  # Delay between sends
        
        return jsonify({
            "status": "success",
            "results": results
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

def init_scheduler():
    """Initialize the scheduler in a separate thread"""
    scheduler_thread = threading.Thread(target=start_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()
