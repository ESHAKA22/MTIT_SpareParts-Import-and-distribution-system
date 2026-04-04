import sys
import os

# Add the shared directory to Python path
shared_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'shared')
if shared_path not in sys.path:
    sys.path.append(shared_path)

try:
    from auth import verify_token, get_current_user
except ImportError:
    # Fallback if shared module not found
    from fastapi import HTTPException, Depends, status
    from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
    from jose import jwt, JWTError
    from datetime import datetime, timedelta
    import os
    from dotenv import load_dotenv

    load_dotenv()
    
    SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")
    ALGORITHM = "HS256"
    security = HTTPBearer()

    def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
        try:
            token = credentials.credentials
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email = payload.get("sub")
            
            if email is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token: missing email",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            return {"email": email}
        
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def get_current_user(user_data: dict = Depends(verify_token)):
        return user_data
