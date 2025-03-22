from project_api.db import get_db_connection
from datetime import datetime

class DatabaseService:
    @staticmethod
    def get_pending_orders():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT p.id_input, a.nama AS nama_admin, pr.nama_produk, 
                       DATE(p.timestamp) AS inputan_masuk, p.deadline, 
                       p.qty AS Jumlah_pcs, p.status_print, p.status_produksi
                FROM table_pesanan p
                JOIN table_produk pr ON p.id_produk = pr.id_produk
                JOIN table_admin a ON p.id_admin = a.ID
                WHERE p.status_produksi = '-' OR p.status_print = '-'
                ORDER BY p.deadline ASC
            """)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()