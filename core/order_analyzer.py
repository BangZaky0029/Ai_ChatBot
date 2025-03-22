from datetime import datetime
from ..services.database_service import DatabaseService
from ..utils.date_utils import DateUtils

class OrderAnalyzer:
    def __init__(self):
        self.db_service = DatabaseService()
        self.data = self.db_service.get_pending_orders()
        self.all_orders = [item for item in self.data]
        self.total_orders = len(self.all_orders)
        self.total_qty = sum(int(item['qty']) for item in self.all_orders)

    def analyze_platform_data(self, platform_name, id_admin=None):
        """Analyze orders for specific platform and admin"""
        if id_admin:
            platform_orders = [item for item in self.data if item['platform'] == platform_name and item['id_admin'] == id_admin]
        else:
            platform_orders = [item for item in self.data if item['platform'] == platform_name]
        
        return self._calculate_platform_metrics(platform_orders, platform_name)

    def _calculate_platform_metrics(self, platform_orders, platform_name):
        """Calculate metrics for platform orders"""
        total_qty = sum(int(item['qty']) for item in platform_orders)
        orders_by_id = {}
        status_count = {'EDITING': 0, '-': 0}
        produksi_count = {'EDITING': 0, '-': 0}

        for order in platform_orders:
            if order['id_pesanan'] not in orders_by_id:
                orders_by_id[order['id_pesanan']] = 0
            orders_by_id[order['id_pesanan']] += int(order['qty'])
            
            status_count[order['status_print']] = status_count.get(order['status_print'], 0) + 1
            produksi_count[order['status_produksi']] = produksi_count.get(order['status_produksi'], 0) + 1

        urgent_deadlines = self._get_urgent_deadlines(platform_orders)
        
        return {
            'platform': platform_name,
            'total_orders': len(platform_orders),
            'unique_pesanan': len(orders_by_id),
            'total_qty': total_qty,
            'qty_by_pesanan': orders_by_id,
            'urgent_deadlines': urgent_deadlines,
            'status_print': status_count,
            'status_produksi': produksi_count
        }

    def _get_urgent_deadlines(self, orders):
        """Get orders with urgent deadlines (≤ 2 days)"""
        today = datetime.now().date()
        urgent_deadlines = []
        for order in orders:
            deadline = datetime.strptime(str(order['deadline']), '%Y-%m-%d').date()
            days_remaining = (deadline - today).days
            if days_remaining <= 2:
                urgent_deadlines.append((order['id_input'], order['id_pesanan'], days_remaining))
        return urgent_deadlines

    def analyze_whatsapp_by_admin(self, id_admin):
        """Analyze WhatsApp orders for specific admin"""
        wa_orders = [item for item in self.data if item['platform'] == 'WhatsApp' and item['id_admin'] == id_admin]
        return self._calculate_whatsapp_metrics(wa_orders)

    def _calculate_whatsapp_metrics(self, wa_orders):
        """Calculate metrics for WhatsApp orders"""
        total_qty = sum(int(item['qty']) for item in wa_orders)
        
        status_count = {'EDITING': 0, '-': 0}
        produksi_count = {'EDITING': 0, '-': 0}
        
        for order in wa_orders:
            status_count[order['status_print']] = status_count.get(order['status_print'], 0) + 1
            produksi_count[order['status_produksi']] = produksi_count.get(order['status_produksi'], 0) + 1

        return {
            'total_orders': len(wa_orders),
            'total_qty': total_qty,
            'status_print': status_count,
            'status_produksi': produksi_count
        }

    def analyze_products(self):
        """Analyze product statistics"""
        product_stats = {}
        deadline_stats = {}
        
        for order in self.data:
            product_name = order['nama_produk']
            qty = int(order['qty'])
            days_remaining = DateUtils.get_days_remaining(order['deadline'])
            
            # Update product stats
            if product_name not in product_stats:
                product_stats[product_name] = 0
            product_stats[product_name] += qty
            
            # Update deadline stats
            deadline_str = order['deadline'].strftime('%Y-%m-%d')
            if deadline_str not in deadline_stats:
                deadline_stats[deadline_str] = {'total_qty': 0, 'products': {}}
            
            deadline_stats[deadline_str]['total_qty'] += qty
            if product_name not in deadline_stats[deadline_str]['products']:
                deadline_stats[deadline_str]['products'][product_name] = 0
            deadline_stats[deadline_str]['products'][product_name] += qty

        return {'product_stats': product_stats, 'deadline_stats': deadline_stats}

    def analyze_pending_by_deadline(self):
        """Analyze pending orders grouped by deadline"""
        deadline_groups = {}
        
        for order in self.data:
            deadline = order['deadline'].strftime('%Y-%m-%d')
            
            if deadline not in deadline_groups:
                deadline_groups[deadline] = {
                    'total_pending': 0,
                    'pending_print': 0,
                    'pending_produksi': 0,
                    'orders': []
                }
            
            group = deadline_groups[deadline]
            if order['status_print'] == '-':
                group['pending_print'] += 1
            if order['status_produksi'] == '-':
                group['pending_produksi'] += 1
            group['total_pending'] = max(group['pending_print'], group['pending_produksi'])
            
            group['orders'].append({
                'id_input': order['id_input'],
                'nama_admin': order['nama_admin'],
                'nama_produk': order['nama_produk'],
                'qty': order['qty'],
                'status_print': order['status_print'],
                'status_produksi': order['status_produksi']
            })
        
        return deadline_groups