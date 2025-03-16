from datetime import datetime
from ..config.wa_config import NOMER_1, NOMER_2, NOMER_3
from .deepSeekAi import get_ai_response
from project_api.db import get_db_connection

def get_data_from_db():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT id_input, id_pesanan, id_admin, platform, qty, status_print, status_produksi, deadline
            FROM table_pesanan
            WHERE status_print = 'EDITING' 
             AND status_produksi = '-'
            ORDER BY deadline ASC
        """)
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

def analyze_platform_data(data, platform_list):
    platform_orders = [item for item in data if item['platform'] in platform_list]
    total_qty = sum(int(item['qty']) for item in platform_orders)
    orders_by_id = {}
    for order in platform_orders:
        if order['id_pesanan'] not in orders_by_id:
            orders_by_id[order['id_pesanan']] = 0
        orders_by_id[order['id_pesanan']] += int(order['qty'])
    
    today = datetime.now().date()
    urgent_deadlines = []
    for order in platform_orders:
        deadline = datetime.strptime(str(order['deadline']), '%Y-%m-%d').date()
        days_remaining = (deadline - today).days
        if days_remaining <= 2:  # Consider orders with 2 or fewer days remaining as urgent
            urgent_deadlines.append((order['id_input'], days_remaining))
    
    return {
        'total_orders': len(platform_orders),
        'unique_pesanan': len(orders_by_id),
        'total_qty': total_qty,
        'qty_by_pesanan': orders_by_id,
        'urgent_deadlines': urgent_deadlines
    }

def create_messages():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = get_data_from_db()
    
    # Analysis for NOMER_1 (Shopee)
    shopee_analysis = analyze_platform_data(data, ['Shopee'])
    admin_prompt = f"""Create a professional summary for Shopee orders:
    - Total orders: {shopee_analysis['total_orders']}
    - Unique orders: {shopee_analysis['unique_pesanan']}
    - Total quantity: {shopee_analysis['total_qty']}
    - Urgent deadlines: {shopee_analysis['urgent_deadlines']}
    Please create a concise, formal message highlighting these points and any urgent deadlines."""
    
    # Analysis for NOMER_2 (TikTok, Tokopedia, Lazada)
    marketplace_analysis = analyze_platform_data(data, ['TikTok', 'Tokopedia', 'Lazada'])
    user_prompt = f"""Create a professional summary for Marketplace orders:
    - Total orders: {marketplace_analysis['total_orders']}
    - Unique orders: {marketplace_analysis['unique_pesanan']}
    - Total quantity: {marketplace_analysis['total_qty']}
    - Urgent deadlines: {marketplace_analysis['urgent_deadlines']}
    Please create a concise, formal message highlighting these points and any urgent deadlines."""
    
    # Analysis for NOMER_3 (Overall summary)
    summary_prompt = f"""Create a comprehensive summary combining:
    Shopee: {shopee_analysis['total_orders']} orders, {shopee_analysis['total_qty']} items
    Marketplace: {marketplace_analysis['total_orders']} orders, {marketplace_analysis['total_qty']} items
    Please create a concise summary of all platforms' status."""
    
    # Get AI responses
    admin_message = get_ai_response(admin_prompt)
    user_message = get_ai_response(user_prompt)
    summary_message = get_ai_response(summary_prompt)
    
    return {
        NOMER_1: f"{admin_message}\n\nSent at: {current_time}",
        NOMER_2: f"{user_message}\n\nSent at: {current_time}",
        NOMER_3: f"{summary_message}\n\nSent at: {current_time}"
    }
