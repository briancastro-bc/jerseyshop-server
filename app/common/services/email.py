from typing import List, Optional

from fastapi import HTTPException
from aiosmtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.config import settings
import asyncio

"""
    :class EmailService - defines properties and methods that can be used for
    emails sending.
"""
class EmailService:
    
    def __init__(self) -> None:
        self._server = SMTP()
    
    """
        Start connection with SMTP server.
    """
    async def _connect_server(self):
        await self._server.connect(
            hostname=settings.SMTP_HOSTNAME,
            port=settings.SMTP_TLS_PORT,
            timeout=200
        )
        await self._server.starttls()
        await self._server.login(
            username=settings.SMTP_USERNAME,
            password=settings.SMTP_PASSWORD,
        )
    
    async def send_email(self, emails: List[str], subject: Optional[str]=None, **kwargs):
        await self._connect_server()
        for email in emails:
            mime = MIMEMultipart()
            mime['From'] = settings.SMTP_USERNAME
            mime['Subject'] = subject if subject is not None else "No-reply"
            mime['To'] = email
            format = MIMEText(kwargs['message'], kwargs['format'])
            mime.attach(format)
            try:
                await self._server.sendmail(settings.SMTP_USERNAME, email, mime.as_string())
            except Exception as e:
                raise HTTPException(400, {
                    "status": "fail",
                    "data": {
                        "message": "fail to send email",
                        "exception": f"{e}"
                    }
                })
        await self._disconnect_server()
    
    async def _disconnect_server(self):
        await self._server.quit()
