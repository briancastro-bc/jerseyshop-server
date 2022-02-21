from sqlalchemy import Column, String, CHAR, TIMESTAMP, Boolean

from app.core.database import Base

import uuid, datetime

class Advertisement(Base):
    __tablename__ = 'advertisements'
    uid = Column(String(36), primary_key=True, nullable=False)
    title = Column(CHAR(40), nullable=True)
    hyperlink = Column(String(400), nullable=True)
    description = Column(String(300), nullable=False)
    time_ago = Column(TIMESTAMP(True), nullable=False, default=datetime.datetime.utcnow())
    is_active = Column(Boolean, nullable=False, default=True)
    is_public = Column(Boolean, nullable=False, default=True)
    
    def __init__(
        self,
        description: str,
        hyperlink: str=None,
        title: str=None
    ) -> None:
        super().__init__()
        self.uid = self.generate_uuid()
        self.title = title
        self.hyperlink = hyperlink
        self.description = description
        
    def generate_uuid(self):
        return str(uuid.uuid4())