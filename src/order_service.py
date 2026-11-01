orders = {
    "ORD-1001": {
        "customer_name": "Sathish",
        "email": "sathish@example.com",
        "item": "Wireless Earbuds",
        "status": "Shipped",
        "carrier": "BlueDart",
        "tracking": "BD7781234",
        "expected_delivery": "2026-11-04",
    },
    "ORD-1002": {
        "customer_name": "Priya",
        "email": "priya@example.com",
        "item": "Cotton Kurta (Size M)",
        "status": "Processing",
        "carrier": None,
        "tracking": None,
        "expected_delivery": "2026-11-06",
    },
    "ORD-1003": {
        "customer_name": "Arjun",
        "email": "arjun@example.com",
        "item": "Running Shoes",
        "status": "Out for delivery",
        "carrier": "Delhivery",
        "tracking": "DL5520987",
        "expected_delivery": "2026-11-01",
    },
    "ORD-1004": {
        "customer_name": "Meena",
        "email": "meena@example.com",
        "item": "Stainless Steel Water Bottle",
        "status": "Delivered",
        "carrier": "Ecom Express",
        "tracking": "EE3349001",
        "expected_delivery": "2026-10-29",
    },
    "ORD-1005": {
        "customer_name": "Karthik",
        "email": "karthik@example.com",
        "item": "Bluetooth Speaker",
        "status": "Cancelled",
        "carrier": None,
        "tracking": None,
        "expected_delivery": None,
    },
    "ORD-1006": {
        "customer_name": "Divya",
        "email": "divya@example.com",
        "item": "Laptop Backpack",
        "status": "Delayed",
        "carrier": "BlueDart",
        "tracking": "BD7790456",
        "expected_delivery": "2026-11-08",
    },
}


def _get_order(order_id: str):
    # Internal helper. Accepts "ord-1001", " ORD-1001 " etc.
    return orders.get(order_id.strip().upper())


def get_verified_order(order_id: str, email: str):
    """Return the order only if the email matches the one on the order.
    A wrong email and an unknown order both return None, on purpose."""
    order = _get_order(order_id)
    if order is None:
        return None
    if order["email"].lower() != email.strip().lower():
        return None
    return order


def find_order_ids_by_email(email: str) -> list[str]:
    """Return the order IDs placed with this email (empty list if none)."""
    email = email.strip().lower()
    return [oid for oid, o in orders.items() if o["email"].lower() == email]