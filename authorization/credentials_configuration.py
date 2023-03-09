import base64


class CredentialsConfig():
    """class to configure the credentials obtained in Nequi Conecta."""
    def __init__(
            self,
            client_id,
            client_secret,
            api_key,
            api_base_path,
            auth_uri,
            grant_type):

        self.client_id = client_id
        self.client_secret = client_secret
        self.api_key = api_key
        self.api_base_path = api_base_path
        self.auth_uri = auth_uri
        self.grant_type = grant_type

    def clientId(self):
        
        clientId = self.client_id.encode('ascii')
        clientId = base64.b64encode(clientId).decode('utf-8')
        return clientId

    def client_secret(self):
        client_secret = self.client_secret.encode('ascii')
        client_secret = base64.b64encode(client_secret).decode('utf-8')
        return client_secret

    def client_credentials(self):
        """
        method to concatenate and encode clinet_id and
        client_secret in 64 bits requirement of Nequi Api
        to get auth token.
        """
        access = f"{self.client_id}:{self.client_secret}".encode('ascii')
        access = base64.b64encode(access).decode('utf-8')
        return access

    def nequi_api_key(self):
        return self.api_key
