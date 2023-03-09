import requests_async as requests
from datetime import datetime, timedelta

class Auth():
    def __init__(self, CredentialsConfig):
        """
        class to get the access token to be able
        to make requests to the nequi api.
        """
        self.token = None
        self.tokenType = None
        self.expiresAt = None
        self.Credentials = CredentialsConfig

    async def auth(self):
        try:
            authorization = (
                f"{self.Credentials.client_credentials()}")
            headers = {
                "Content-type": "application/x-www-form-urlencoded",
                "Accept": "application/json",
                "Authorization": f"Basic {authorization}"
            }
            endpoint = f"{self.Credentials.auth_uri}?grant_type={self.Credentials.grant_type}"
            try:
                response = await requests.post(f"{endpoint}", headers=headers)
                if (response and response.status_code == 200):
                    response = response.json()
                    self.token = response.get('access_token')
                    self.tokenType = response.get('token_type')
                    self.expiresAt = datetime.now() + timedelta(seconds=response.get('expires_in'))
                else:
                    return {
                'error':'Unable to auth Nequi, please check the information sent'
                }

            except requests.exceptions.ConnectionError as err:
                return {'error': err}
            except requests.exceptions.HTTPError as err:
                return {'error': err}
            except requests.exceptions.RequestException as err:
                return {'error': err}

        except:
            return {
                'error':'Unable to auth Nequi, please check the information sent'
            }

    async def get_token(self):
        if self.is_valid_token() == False:
            await self.auth()
        return f"{self.tokenType} {self.token}"

    def is_valid_token(self):
        if not self.expiresAt or self.expiresAt <= (datetime.now()):
            self.expiresAt = None
            print('Request a new token')
            return False
        return True

    async def refresh(self):
        await self.auth()
        return f"{self.tokenType} {self.token}"