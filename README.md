# Campus Printing Management System

A web-based system to manage printing orders for a campus printing shop. The system automatically calculates costs based on print type and automatically stores orders.

## Features

- **Automatic Cost Calculation**: Automatically computes printing costs based on selected print type and number of pages
- **Order Management**: Create, read, update, and delete printing orders
- **Order Status Tracking**: Track order status (pending, completed, cancelled)
- **Analytics**: View revenue, order summaries, and statistics
- **Local Storage**: All orders stored in JSON file for persistence
- **RESTful API**: Clean API endpoints for all operations

## Printing Prices

| Print Type | Price per Page |
|-----------|-----------------|
| Black & White | ₱2.00 |
| Colored | ₱5.00 |
| Photo Paper | ₱20.00 |

## Installation

### Requirements
- Python 3.8+
- pip (Python package manager)

### Setup Steps

1. Navigate to project directory:
```bash
cd campus_printing_management
```

2. Create virtual environment (optional but recommended):
```bash
python -m venv venv
venv\Scripts\activate # On MAC: source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Server

Start the FastAPI server:

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload
```

The server will start at `http://localhost:8000`

## API Documentation

Once the server is running, access interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Orders

#### Create Order
```
POST /api/orders
```
Request body:
```json
{
  "print_type": "colored",
  "num_pages": 25,
  "client_name": "Jade Micha",
  "notes": "Urgent order"
}
```

#### Get All Orders
```
GET /api/orders
```

#### Get Specific Order
```
GET /api/orders/{order_id}
```

#### Update Order
```
PUT /api/orders/{order_id}
```
Request body (all fields optional):
```json
{
  "print_type": "black_and_white",
  "num_pages": 10,
  "status": "completed",
  "client_name": "Jane Doe",
  "notes": "Updated notes"
}
```

#### Delete Order
```
DELETE /api/orders/{order_id}
```

### Filtering & Analytics

#### Get Orders by Status
```
GET /api/orders/status/{status}
```
Valid statuses: `pending`, `completed`, `cancelled`

#### Get Orders by Print Type
```
GET /api/orders/type/{print_type}
```
Valid types: `black_and_white`, `colored`, `photo_paper`

### Other Endpoints

#### Pricing Information
```
GET /pricing
```

#### Health Check
```
GET /health
```

## Project Structure

```
campus_printing_management/
├── main.py              # FastAPI application entry point
├── models.py            # Pydantic models for requests/responses
├── routes.py            # API route handlers
├── database.py          # Order database (JSON storage)
├── pricing.py           # Pricing calculation logic
├── requirements.txt     # Project dependencies
├── data/
│   └── orders.json      # Orders storage (auto-created)
└── README.md            # This file
```

## Data Storage

Orders are stored in `data/orders.json` using local JSON file storage. The file is automatically created on first run.

