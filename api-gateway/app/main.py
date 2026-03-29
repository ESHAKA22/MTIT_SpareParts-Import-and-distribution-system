import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.openapi.docs import get_swagger_ui_html
import httpx

load_dotenv()

CART_SERVICE_URL = os.getenv("CART_SERVICE_URL", "http://localhost:8001")
PAYMENT_SERVICE_URL = os.getenv("PAYMENT_SERVICE_URL", "http://localhost:8002")
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://localhost:8005")
ORDER_SERVICE_URL = os.getenv("ORDER_SERVICE_URL", "http://localhost:8004")
app = FastAPI(
    title="API Gateway",
    description="Gateway for Cart Service and Payment Service",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


@app.get("/")
def root():
    return {
        "message": "API Gateway is running",
        "routes": {
            "cart": "/cart",
            "payments": "/payments",
            "cart_docs": "/cart/docs",
            "payment_docs": "/payments/docs",
            "users": "/users",
            "user_docs": "/users/docs",
            "orders": "/orders",
"order_docs": "/orders/docs",
            
        }
    }


@app.get("/health")
def health():
    return {"status": "ok", "service": "api-gateway"}



@app.get("/cart/docs", include_in_schema=False)
def cart_docs():
    return get_swagger_ui_html(
        openapi_url="/cart/openapi.json",
        title="Cart Service Docs via Gateway"
    )


@app.get("/payments/docs", include_in_schema=False)
def payment_docs():
    return get_swagger_ui_html(
        openapi_url="/payments/openapi.json",
        title="Payment Service Docs via Gateway"
    )
@app.get("/users/docs", include_in_schema=False)
def user_docs():
    return get_swagger_ui_html(
        openapi_url="/users/openapi.json",
        title="User Service Docs via Gateway"
    )

@app.get("/orders/docs", include_in_schema=False)
def order_docs():
    return get_swagger_ui_html(
        openapi_url="/orders/openapi.json",
        title="Order Service Docs via Gateway"
    )


@app.get("/cart/openapi.json", include_in_schema=False)
async def cart_openapi():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{CART_SERVICE_URL}/openapi.json")
        return JSONResponse(content=response.json(), status_code=response.status_code)


@app.get("/payments/openapi.json", include_in_schema=False)
async def payment_openapi():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{PAYMENT_SERVICE_URL}/openapi.json")
        return JSONResponse(content=response.json(), status_code=response.status_code)

@app.get("/users/openapi.json", include_in_schema=False)
async def user_openapi():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{USER_SERVICE_URL}/openapi.json")
        return JSONResponse(content=response.json(), status_code=response.status_code)

@app.get("/orders/openapi.json", include_in_schema=False)
async def order_openapi():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{ORDER_SERVICE_URL}/openapi.json")
        return JSONResponse(content=response.json(), status_code=response.status_code)

async def proxy_request(request: Request, target_base_url: str, path: str) -> Response:
    async with httpx.AsyncClient() as client:
        target_url = f"{target_base_url}/{path}"

        body = await request.body()
        headers = dict(request.headers)
        headers.pop("host", None)

        proxied_response = await client.request(
            method=request.method,
            url=target_url,
            params=request.query_params,
            content=body,
            headers=headers,
        )

        content_type = proxied_response.headers.get("content-type", "")
        if "application/json" in content_type:
            return JSONResponse(
                content=proxied_response.json(),
                status_code=proxied_response.status_code
            )

        return Response(
            content=proxied_response.content,
            status_code=proxied_response.status_code,
            media_type=content_type
        )



# -----------------------------
# Cart proxy routes
# -----------------------------
@app.api_route("/cart/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_cart(path: str, request: Request):
    return await proxy_request(request, CART_SERVICE_URL, f"cart/{path}")

# -----------------------------
# payments proxy routes
# -----------------------------


@app.api_route("/payments/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_payments(path: str, request: Request):
    return await proxy_request(request, PAYMENT_SERVICE_URL, f"payments/{path}")

# -----------------------------
# User proxy routes
# -----------------------------
@app.api_route("/users", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_users_root(request: Request):
    return await proxy_request(request, USER_SERVICE_URL, "api/users")


@app.api_route("/users/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_users(path: str, request: Request):
    return await proxy_request(request, USER_SERVICE_URL, f"api/users/{path}")

@app.api_route("/orders", methods=["GET", "POST", "PUT", "DELETE", "PATCH"], operation_id="proxy_orders_root")
async def proxy_orders_root(request: Request):
    return await proxy_request(request, ORDER_SERVICE_URL, "orders")


@app.api_route("/orders/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"], operation_id="proxy_orders_path")
async def proxy_orders(path: str, request: Request):
    return await proxy_request(request, ORDER_SERVICE_URL, f"orders/{path}")