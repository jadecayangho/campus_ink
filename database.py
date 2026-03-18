import json
import os
from pathlib import Path
from typing import List, Optional
from datetime import datetime
from models import Order, OrderCreate, OrderUpdate, PrintType
from pricing import calculate_order_cost
import uuid


class OrderDatabase:
    """Local JSON-based storage for orders"""

    def __init__(self, db_file: str = "orders.json"):
        self.db_file = db_file
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)
        self.db_path = self.data_dir / db_file
        self._initialize_db()

    def _initialize_db(self):
        """Initialize the database file if it doesn't exist"""
        if not self.db_path.exists():
            self._save_data([])

    def _load_data(self) -> List[dict]:
        """Load all orders from JSON file"""
        if not self.db_path.exists():
            return []
        try:
            with open(self.db_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

    def _save_data(self, data: List[dict]):
        """Save orders to JSON file"""
        with open(self.db_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)

    def create_order(self, order_create: OrderCreate) -> Order:
        """Create a new order"""
        total_cost = calculate_order_cost(order_create.print_type, order_create.num_pages)

        order_id = str(uuid.uuid4())
        new_order = {
            "id": order_id,
            "print_type": order_create.print_type,
            "num_pages": order_create.num_pages,
            "total_cost": total_cost,
            "created_at": datetime.now().isoformat(),
            "status": "pending",
            "client_name": order_create.client_name,
            "notes": order_create.notes
        }

        orders = self._load_data()
        orders.append(new_order)
        self._save_data(orders)

        return Order(**new_order)

    def get_all_orders(self) -> List[Order]:
        """Get all orders"""
        orders_data = self._load_data()
        return [Order(**order) for order in orders_data]

    def get_order_by_id(self, order_id: str) -> Optional[Order]:
        """Get a specific order by ID"""
        orders_data = self._load_data()
        for order_data in orders_data:
            if order_data["id"] == order_id:
                return Order(**order_data)
        return None

    def update_order(self, order_id: str, order_update: OrderUpdate) -> Optional[Order]:
        """Update an order"""
        orders_data = self._load_data()

        for order_data in orders_data:
            if order_data["id"] == order_id:
                if order_update.print_type is not None:
                    order_data["print_type"] = order_update.print_type
                if order_update.num_pages is not None:
                    order_data["num_pages"] = order_update.num_pages
                if order_update.status is not None:
                    order_data["status"] = order_update.status
                if order_update.client_name is not None:
                    order_data["client_name"] = order_update.client_name
                if order_update.notes is not None:
                    order_data["notes"] = order_update.notes

                if order_update.print_type is not None or order_update.num_pages is not None:
                    print_type = order_data["print_type"]
                    num_pages = order_data["num_pages"]
                    order_data["total_cost"] = calculate_order_cost(print_type, num_pages)

                self._save_data(orders_data)
                return Order(**order_data)

        return None

    def delete_order(self, order_id: str) -> bool:
        """Delete an order"""
        orders_data = self._load_data()
        original_length = len(orders_data)
        orders_data = [order for order in orders_data if order["id"] != order_id]

        if len(orders_data) < original_length:
            self._save_data(orders_data)
            return True
        return False

    def get_orders_by_status(self, status: str) -> List[Order]:
        """Get all orders with a specific status"""
        orders_data = self._load_data()
        return [Order(**order) for order in orders_data if order["status"] == status]

    def get_orders_by_print_type(self, print_type: PrintType) -> List[Order]:
        """Get all orders for a specific print type"""
        orders_data = self._load_data()
        return [Order(**order) for order in orders_data if order["print_type"] == print_type]

    def get_total_revenue(self) -> float:
        """Calculate total revenue from all completed orders"""
        orders_data = self._load_data()
        total = sum(
            order["total_cost"] for order in orders_data
            if order["status"] == "completed"
        )
        return total
