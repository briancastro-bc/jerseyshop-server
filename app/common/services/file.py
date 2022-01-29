from enum import Enum
from typing import Optional

class RSAKeyType(Enum):
    PRIVATE='priv'
    PUBLIC='pub'

class FileService:
    
    @staticmethod
    def getRSAKey(key_type: RSAKeyType):
        key_path: str = f'app/common/keys/{key_type}key.pem'
        with open(key_path, 'rb') as f:
            key: Optional[str] = f.read()
        return key