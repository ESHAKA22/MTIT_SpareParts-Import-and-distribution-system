# SpareParts Import and Sales System

A microservices-based e-commerce platform for managing spare parts operations with JWT authentication integration.

## Architecture

### Services
- **API Gateway** (Port 8000) - Central entry point and request routing
- **User Service** (Port 8005) - User authentication and management
- **Cart Service** (Port 8001) - Shopping cart functionality
- **Order Service** (Port 8004) - Order processing and management
- **Payment Service** (Port 8002) - Payment processing
- **Catalogue Service** (Port 8009) - Product catalog management
- **Complaint Service** (Port 8008) - Customer complaint handling

### Technology Stack
- FastAPI for all services
- MongoDB for data storage
- JWT authentication
- Microservices architecture

## Authentication Flow

1. **User Registration/Login**: Users register/login through the User Service
2. **JWT Token Generation**: User Service generates JWT tokens upon successful authentication
3. **Token Validation**: All other services validate JWT tokens using shared authentication middleware
4. **User Context**: Services extract user email from JWT token for personalized operations

## API Endpoints

### Authentication
- `POST /users/register` - Register new user
- `POST /users/login` - User login (returns JWT token)

### Protected Endpoints (require JWT token)
All endpoints except health checks and user registration/login require JWT authentication:

#### Cart Operations
- `GET /cart/` - Get user's cart
- `POST /cart/add` - Add item to cart
- `PUT /cart/item/{item_id}` - Update cart item
- `DELETE /cart/item/{item_id}` - Remove cart item
- `DELETE /cart/clear` - Clear cart

#### Order Operations
- `POST /orders/create` - Create order
- `GET /orders/` - Get user's orders
- `GET /orders/{order_id}` - Get specific order

#### Payment Operations
- `POST /payments/process` - Process payment
- `GET /payments/{payment_id}` - Get payment details
- `GET /payments/customer/{customer_id}` - Get customer payments

#### Catalogue Operations
- `GET /catalogue/` - Browse products (public)
- `POST /catalogue/` - Add product (admin)
- `PUT /catalogue/{product_id}` - Update product (admin)
- `DELETE /catalogue/{product_id}` - Delete product (admin)

#### Complaint Operations
- `POST /complaints/` - Create complaint
- `GET /complaints/` - Get user's complaints
- `GET /complaints/customer/{customer_id}` - Get customer complaints

## Usage

### 1. Start all services
```bash
# Navigate to each service directory and run:
uvicorn app.main:app --port <PORT> --reload
```

### 2. Register/Login
```bash
# Register user
curl -X POST http://localhost:8000/users/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123", "name": "John Doe"}'

# Login (get JWT token)
curl -X POST http://localhost:8000/users/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'
```

### 3. Use JWT token for authenticated requests
```bash
# Use the token from login response
TOKEN="your_jwt_token_here"

# Add item to cart
curl -X POST http://localhost:8000/cart/add \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"product_id": "PRD001", "product_name": "Tractor Brake Pad", "unit_price": 2500.00, "quantity": 2}'
```

## Security Features

- JWT token-based authentication
- User isolation (users can only access their own data)
- Authorization header forwarding through API Gateway
- Token expiration (1 hour)
- Password hashing with bcrypt

## Development

### Environment Variables
Each service requires:
- `MONGO_URL` - MongoDB connection string
- `SECRET_KEY` - JWT signing key (same across all services)

### Shared Authentication
The `shared/auth.py` module provides:
- `verify_token()` - JWT token validation
- `get_current_user()` - User context extraction

## Database Collections
- `users` - User accounts and credentials
- `carts` - Shopping cart items
- `orders` - Order records
- `payments` - Payment transactions
- `products` - Product catalog
- `complaints` - Customer complaints
