from datetime import datetime
from collections import defaultdict
from ..services.database_service import DatabaseService

class MessageGenerator:
    def __init__(self):
        self.db_service = DatabaseService()
        self.data = self.db_service.get_pending_orders()  # Initialize data in constructor

    def generate_summary(self):
        orders = self.db_service.get_pending_orders()
        if not orders:
            return "✅ Tidak ada pesanan pending saat ini."

        # Group orders by deadline
        deadline_groups = defaultdict(lambda: {'print': 0, 'produksi': 0})
        for order in orders:
            deadline = order['deadline'].strftime('%d-%m-%Y')
            if order['status_print'] == '-':
                deadline_groups[deadline]['print'] += 1
            if order['status_produksi'] == '-':
                deadline_groups[deadline]['produksi'] += 1

        # Generate summary message
        summary = ["📋 RINGKASAN STATUS PESANAN:\n"]
        
        for deadline, counts in sorted(deadline_groups.items()):
            summary.append(f"📅 Deadline: {deadline}")
            if counts['print'] > 0:
                summary.append(f"• Pending Print: {counts['print']} pesanan")
            if counts['produksi'] > 0:
                summary.append(f"• Pending Produksi: {counts['produksi']} pesanan")
            
            # Add urgent warning for near deadlines
            order_date = datetime.strptime(deadline, '%d-%m-%Y').date()
            days_remaining = (order_date - datetime.now().date()).days
            
            if days_remaining <= 2:
                summary.append("⚠️ URGENT! Mohon segera diproses!")
            
            summary.append("")  # Add empty line between deadlines

        return "\n".join(summary)

    def generate_message(self, admin_id=None):
        """Generate simple message for pending orders"""
        orders = self.db_service.get_pending_orders()  # Get fresh data
        if admin_id:
            orders = [order for order in orders if order['id_admin'] == admin_id]
            
        if not orders:
            return "✅ Tidak ada pesanan pending saat ini."

        message = ["📋 Ringkasan Order Pending:"]
        
        for order in orders:
            deadline = datetime.strptime(str(order['deadline']), '%Y-%m-%d')
            deadline_str = deadline.strftime('%d-%m-%Y')
            
            message.append(f"\n📅 Deadline: {deadline_str}")
            message.append(f"• Produk: {order['nama_produk']}")
            message.append(f"• Jumlah: {order['Jumlah_pcs']} pcs")
            message.append(f"• Status Print: {order['status_print']}")
            message.append(f"• Status Produksi: {order['status_produksi']}")

        return "\n".join(message)

    # Remove _get_pending_orders method as it's no longer needed