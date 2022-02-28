from fastapi import Request
from authlib.integrations.starlette_client import OAuth

class OAuth2Service:
    
    def __init__(self, provider: str, **kwargs) -> None:
        self.oauth = OAuth()
        self.oauth.register(
            provider,
            overwrite=True,
            **kwargs
        )
    
    async def google_login(self, request: Request):
        #print(request.url)
        redirect_uri = request.url_for('google_authorize')
        return await self.oauth.google.authorize_redirect(request, redirect_uri)
    
    async def google_authorize(self, request: Request):
        token = await self.oauth.google.authorize_access_token(request)
        user = await self.oauth.google.parse_id_token(request, token)
        return dict(user)