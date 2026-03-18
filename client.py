#!/usr/bin/env python
import sys
import requests
import json
from fastapi import HTTPException

BASE_URL = "http://127.0.0.1:8000/api/orders"

def print_success(message, data=None):
    print(f"\nSuccess: {message}")
    if data is not None:
        print(json.dumps(data, indent=2))
    print("")

def order(args):
    # least expected arguments: ['<client_name>', '<print_type>', '<num_pages>']
    # Optional: ['<client_name>', '<print_type>', '<num_pages>', '<notes>']
    # Print types input: black_and_white, colored, photo_paper
    if len(args) < 4:
        raise HTTPException(
            status_code=400, 
            detail="Invalid format. Usage: python client.py order <client_name> <print_type> <num_pages> [notes]"
        )
    
    client_name = args[1]
    print_type = args[2]
    
    try:
        num_pages = int(args[3])
        if num_pages <= 0:
            raise ValueError
    except ValueError:
        raise HTTPException(status_code=400, detail="Number of pages must be a positive integer.")

    notes = args[4] if len(args) > 4 else None

    payload = {
        "client_name": client_name,
        "print_type": print_type,
        "num_pages": num_pages
    }
    
    if notes:
        payload["notes"] = notes

    try:
        response = requests.post(f"{BASE_URL}/", json=payload)
        if response.status_code == 201:
            print_success("Order created successfully!", response.json())
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json().get('detail', response.text))
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Could not connect to the server.")

def view():
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print_success("Retrieving all orders...", response.json())
        else:
            raise HTTPException(status_code=response.status_code, detail="Failed to retrieve orders")
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Could not connect to the server.")

def search(args):
    if len(args) < 2:
        raise HTTPException(status_code=400, detail="Invalid format. Usage: python client.py search <order_id>")
    
    order_id = args[1]
    try:
        response = requests.get(f"{BASE_URL}/{order_id}")
        if response.status_code == 200:
            print_success(f"Order {order_id} found:", response.json())
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json().get('detail', response.text))
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Could not connect to the server.")

def update(args):
    if len(args) < 3:
        raise HTTPException(status_code=400, detail="Invalid format. Usage: python client.py update <order_id> <status>")
    
    order_id = args[1]
    status_update = args[2].lower()
    
    payload = {"status": status_update}
    
    try:
        response = requests.put(f"{BASE_URL}/{order_id}", json=payload)
        if response.status_code == 200:
            print_success(f"Order {order_id} updated successfully!", response.json())
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json().get('detail', response.text))
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Could not connect to the server.")

def delete(args):
    if len(args) < 2:
        raise HTTPException(status_code=400, detail="Invalid format. Usage: python client.py delete <order_id>")
    
    order_id = args[1]
    try:
        response = requests.delete(f"{BASE_URL}/{order_id}")
        if response.status_code == 204:
            print_success(f"Order {order_id} deleted successfully!")
        else:
            raise HTTPException(status_code=response.status_code, detail=f"Failed to delete order. Status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Could not connect to the server.")

def filter_status(args):
    if len(args) < 2:
        raise HTTPException(status_code=400, detail="Invalid format. Usage: python client.py status <pending|completed|cancelled>")
    
    status = args[1].lower()
    try:
        response = requests.get(f"{BASE_URL}/status/{status}")
        if response.status_code == 200:
            print_success(f"Orders with status '{status}':", response.json())
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json().get('detail', response.text))
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Could not connect to the server.")

def filter_type(args):
    if len(args) < 2:
        raise HTTPException(status_code=400, detail="Invalid format. Usage: python client.py type <print_type>")
    
    print_type = args[1]
    try:
        response = requests.get(f"{BASE_URL}/type/{print_type}")
        if response.status_code == 200:
            print_success(f"Orders of type '{print_type}':", response.json())
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json().get('detail', response.text))
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Could not connect to the server.")
    


def main():
    if len(sys.argv) < 2:
        print("\nCampusInk CLI Client")
        print("Usage: python client.py <command> [arguments]")
        print("Commands:")
        print("  order <client_name> <type> <pages> [notes]  - Create a new printing order")
        print("  view                                        - View all orders")
        print("  search <id>                                 - Search for a specific order by ID")
        print("  update <id> <status>                        - Update an order's status")
        print("  delete <id>                                 - Delete an order")
        print("  status <status_name>                        - View orders by status")
        print("  type <print_type>                           - View orders by print type\n")
        sys.exit(1)

    cmnd = sys.argv[1].lower()

    try:
        if cmnd == "order":
            order(sys.argv[1:])
        elif cmnd == "search":
            search(sys.argv[1:])
        elif cmnd == "view":
            view()
        elif cmnd == "update":
            update(sys.argv[1:])
        elif cmnd == "delete":
            delete(sys.argv[1:])
        elif cmnd == "status":
            filter_status(sys.argv[1:])
        elif cmnd == "type":
            filter_type(sys.argv[1:])
        else:
            raise HTTPException(status_code=400, detail=f"Unknown command '{cmnd}'.")
            
    except HTTPException as e:
        print(f"\nError {e.status_code}: {e.detail}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected Error: {str(e)}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()