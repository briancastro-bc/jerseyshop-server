from enum import Enum
from typing import Optional, Any

from fastapi import UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import pandas, os, sys, openpyxl

class RSAKeyType(Enum):
    PRIVATE='priv'
    PUBLIC='pub'

class FileType(Enum):
    format='formats'
    images='images'

class FileService:
    
    __allowed_files__: dict[str, Any] = {
        'formats': ['xls', 'xlsx', 'pdf', 'cv'],
        'images': ['png', 'jpg', 'jpeg', 'svg']
    }
    
    @staticmethod
    def getRSAKey(key_type: RSAKeyType):
        key_path: str = f'app/common/keys/{key_type}key.pem'
        with open(key_path, 'rb') as f:
            key: Optional[str] = f.read()
        return key
    
    def upload_file(self, file: UploadFile):
        try:
            return
        except Exception:
            pass

    @classmethod
    async def import_excel_file(cls, file: UploadFile, db: AsyncSession, **kwargs):
        try:
            if cls._is_allowed(file.filename, FileType.format):
                if '.xls' in file.filename:
                    #read_file = pandas.read_excel('https://docs.google.com/spreadsheets/d/1IR2pZTYoa5dRASBLgF_yoc4I6kGHNylj/edit?usp=sharing&ouid=110257168752293269631&rtpof=true&sd=true', engine='openpyxl')
                    read = ""
                    return read
                pass
            else:
                return None
        except Exception as e:
            raise HTTPException(
                400,
                {
                    "status": "fail",
                    "data": {
                        "exception": f"{e}"
                    }
                }
            )
    
    @classmethod
    async def export_excel_file(cls):
        pass

    @classmethod
    def _is_allowed(cls, filename: str or bytes, file_type: FileType) -> bool:
        return filename.split('.')[1] in cls.__allowed_files__[file_type.value]