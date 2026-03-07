from fastapi import APIRouter, HTTPException, status
from models import Order, OrderCreate, OrderUpdate, PrintType
from database import OrderDatabase
from pricing import get_all_prices

router = APIRouter(prefix="/api/orders", tags=["orders"])
db = OrderDatabase()


@router.post("/", response_model=Order, status_code=status.HTTP_201_CREATED)
def create_order(order_create: OrderCreate):
    """Create a new printing order. System automatically calculates cost."""
    try:
        order = db.create_order(order_create)
        return order
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating order: {str(e)}"
        )


@router.get("/", response_model=list[Order])
def get_all_orders():
    """Retrieve all printing orders"""
    orders = db.get_all_orders()
    return orders


@router.get("/{order_id}", response_model=Order)
def get_order(order_id: str):
    """Retrieve a specific order by ID"""
    order = db.get_order_by_id(order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID {order_id} not found"
        )
    return order


@router.put("/{order_id}", response_model=Order)
def update_order(order_id: str, order_update: OrderUpdate):
    """Update an existing order details"""
    updated_order = db.update_order(order_id, order_update)
    if not updated_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID {order_id} not found"
        )
    return updated_order


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: str):
    """Delete an order"""
    success = db.delete_order(order_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID {order_id} not found"
        )
    return None


@router.get("/status/{status}", response_model=list[Order])
def get_orders_by_status(status: str):
    """Get all orders with a specific status (pending, completed, cancelled)"""
    valid_statuses = {"pending", "completed", "cancelled"}
    if status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Must be one of: {valid_statuses}"
        )
    orders = db.get_orders_by_status(status)
    return orders


@router.get("/type/{print_type}", response_model=list[Order])
def get_orders_by_print_type(print_type: PrintType):
    """Get all orders for a specific print type"""
    try:
        orders = db.get_orders_by_print_type(print_type)
        return orders
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid print type: {print_type}"
        )


# @router.get("/analytics/revenue", response_model=dict)
# def get_total_revenue():
#     """Get total revenue from completed orders"""
#     total = db.get_total_revenue()
#     return {
#         "total_revenue": total,
#         "currency": "PHP"
#     }


# @router.get("/analytics/summary", response_model=dict)
# def get_orders_summary():
#     """Get summary of all orders"""
#     all_orders = db.get_all_orders()
#     pending_orders = db.get_orders_by_status("pending")
#     completed_orders = db.get_orders_by_status("completed")
#     total_revenue = db.get_total_revenue()

#     total_pages = sum(order.num_pages for order in all_orders)
#     total_cost = sum(order.total_cost for order in all_orders)

#     return {
#         "total_orders": len(all_orders),
#         "pending_orders": len(pending_orders),
#         "completed_orders": len(completed_orders),
#         "total_pages_ordered": total_pages,
#         "total_cost_of_all_orders": total_cost,
#         "revenue_from_completed": total_revenue,
#         "currency": "PHP"
#     }
