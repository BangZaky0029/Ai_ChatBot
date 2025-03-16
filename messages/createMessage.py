from datetime import datetime
from ..config.wa_config import NOMER_1, NOMER_2, NOMER_3
from .deepSeekAi import get_ai_response
from project_api.db import get_db_connection

# Mengambil data dari database
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

# Analisis data berdasarkan platform
def analyze_platform_data(data, platform_name):
    platform_orders = [item for item in data if item['platform'] == platform_name]
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
        if days_remaining <= 2:
            urgent_deadlines.append((order['id_input'], order['id_pesanan'], days_remaining))
    
    return {
        'platform': platform_name,
        'total_orders': len(platform_orders),
        'unique_pesanan': len(orders_by_id),
        'total_qty': total_qty,
        'qty_by_pesanan': orders_by_id,
        'urgent_deadlines': urgent_deadlines
    }

# Fungsi untuk membuat pesan
def generate_message(analysis, platform_name):
    if analysis['total_orders'] == 0:
        return f"Alhamdulillah, Orderan {platform_name} sudah update semua."

    deadline_messages = []
    for item in analysis['urgent_deadlines']:
        id_input, id_pesanan, days_remaining = item
        if days_remaining == 0:
            deadline_messages.append(f"- Order {id_input} (Pesanan {id_pesanan}) harus selesai hari ini.")
        elif days_remaining == 1:
            deadline_messages.append(f"- Order {id_input} (Pesanan {id_pesanan}) harus selesai besok.")
        else:
            deadline_messages.append(f"- Order {id_input} (Pesanan {id_pesanan}) harus selesai dalam {days_remaining} hari.")

    deadline_message = "\n".join(deadline_messages) if deadline_messages else "Tidak ada orderan mendesak."
    
    message = (
        f"Platform: {platform_name}\n"
        f"Jumlah Order: {analysis['total_orders']}\n"
        f"Jumlah Pesanan Unik: {analysis['unique_pesanan']}\n"
        f"Jumlah Qty: {analysis['total_qty']}\n"
        f"Rincian Urgensi:\n{deadline_message}\n\n"
        "Mohon segera konfirmasi jika ada order yang perlu diprioritaskan. Terima kasih."
    )
    return message

# Fungsi untuk membuat semua pesan dan mengirim ke nomor tujuan
def create_messages():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = get_data_from_db()

    # Analisis per platform
    shopee_analysis = analyze_platform_data(data, "Shopee")
    tiktok_analysis = analyze_platform_data(data, "TikTok")
    tokopedia_analysis = analyze_platform_data(data, "Tokopedia")
    lazada_analysis = analyze_platform_data(data, "Lazada")

    # Buat pesan untuk setiap platform
    message_shopee = generate_message(shopee_analysis, "Shopee")
    message_tiktok = generate_message(tiktok_analysis, "TikTok")
    message_tokopedia = generate_message(tokopedia_analysis, "Tokopedia")
    message_lazada = generate_message(lazada_analysis, "Lazada")

    # Buat rekap keseluruhan untuk NOMER_3
    summary_message = (
        f"Rekap Keseluruhan Orderan:\n\n"
        f"- Shopee: {shopee_analysis['total_orders']} order ({shopee_analysis['total_qty']} item)\n"
        f"- TikTok: {tiktok_analysis['total_orders']} order ({tiktok_analysis['total_qty']} item)\n"
        f"- Tokopedia: {tokopedia_analysis['total_orders']} order ({tokopedia_analysis['total_qty']} item)\n"
        f"- Lazada: {lazada_analysis['total_orders']} order ({lazada_analysis['total_qty']} item)\n\n"
        f"Silakan cek dan prioritaskan order sesuai urgensi. Terima kasih."
    )

    # Kirim pesan
    return {
        NOMER_1: f"{message_shopee}\n\nSent at: {current_time}",
        NOMER_2: f"{message_tiktok}\n\n{message_tokopedia}\n\n{message_lazada}\n\nSent at: {current_time}",
        NOMER_3: f"{summary_message}\n\nSent at: {current_time}"
    }
