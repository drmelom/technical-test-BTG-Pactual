from datetime import datetime, timedelta
from typing import Optional, Any, Union

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request

from app.core.config import settings


class Security:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    security = HTTPBearer()

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return cls.pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        """Generate password hash."""
        return cls.pwd_context.hash(password)

    @classmethod
    def create_access_token(
        cls, 
        subject: Union[str, Any], 
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create access token."""
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        
        to_encode = {
            "exp": expire,
            "iat": datetime.utcnow(),
            "sub": str(subject),
            "type": "access"
        }
        
        encoded_jwt = jwt.encode(
            to_encode, 
            settings.SECRET_KEY, 
            algorithm=settings.ALGORITHM
        )
        return encoded_jwt

    @classmethod
    def create_refresh_token(
        cls, 
        subject: Union[str, Any], 
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create refresh token."""
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
            )
        
        to_encode = {
            "exp": expire,
            "iat": datetime.utcnow(),
            "sub": str(subject),
            "type": "refresh"
        }
        
        encoded_jwt = jwt.encode(
            to_encode, 
            settings.SECRET_KEY, 
            algorithm=settings.ALGORITHM
        )
        return encoded_jwt

    @classmethod
    def decode_token(cls, token: str) -> dict:
        """Decode and validate token."""
        try:
            payload = jwt.decode(
                token, 
                settings.SECRET_KEY, 
                algorithms=[settings.ALGORITHM]
            )
            return payload
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

    @classmethod
    def get_current_user_id(cls, credentials: HTTPAuthorizationCredentials) -> str:
        """Get current user ID from token."""
        token = credentials.credentials
        payload = cls.decode_token(token)
        
        user_id = payload.get("sub")
        token_type = payload.get("type")
        
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if token_type != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        return str(user_id)

    @classmethod
    def validate_refresh_token(cls, token: str) -> str:
        """Validate refresh token and return user ID."""
        payload = cls.decode_token(token)
        
        user_id = payload.get("sub")
        token_type = payload.get("type")
        
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
        
        if token_type != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
            )
            
        return str(user_id)


# Create instance
security = Security()
