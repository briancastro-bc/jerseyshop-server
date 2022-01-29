from fastapi import HTTPException

from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.common.models import UserCreate, UserBase
from app.core.schemas import User

class AuthService:
    
    def __init__(self) -> None:
        self.password_ctx: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    def register(self, user: UserCreate, db: Session):
        db_user = db.query(User).filter_by(email=user.email_address).first()
        if not db_user or db_user is None:
            hash_password: str = self._get_password_hash(user.password)
            try:
                new_user = User(
                    email=user.email_address, 
                    password=hash_password, 
                    name=user.name, 
                    last_name=user.last_name, 
                    birthday=user.birthday, 
                    accept_advertising=user.accept_advertising, 
                    accept_terms=user.accept_terms
                )
                db.add(new_user)
                db.commit()
                # db.refresh(new_user)
                return new_user
            except Exception as e:
                raise HTTPException(status_code=400, detail={
                    "status": "fail",
                    "data": {
                        "message": "Ocurrio un error",
                        "exception": "{}".format(e)
                    }
                })
        return None
    
    def login(self, user: UserBase, db: Session):
        db_user = db.query(User).filter_by(email=user.email_address).first()
        if db_user:
            verify_password = self._verify_password(user.password, db_user.password)
            if verify_password:
                return db_user
            return None
        return None
    
    def _get_password_hash(self, password: str):
        return self.password_ctx.hash(password)
    
    def _verify_password(self, plain_password: str or bytes, h_password: str or bytes):
        return self.password_ctx.verify(plain_password, h_password)
    