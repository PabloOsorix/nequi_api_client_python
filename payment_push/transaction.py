from .cancel_unregistered_payment import CancelUnregisteredPaymentPush
from .get_status_payment import GetStatusPayment
from .unregistered_payment_request import UnregisteredPaymentRequest
from ..authorization.credentials_configuration import CredentialsConfig
import asyncio


class Transaction():
    """
    class compose by classes that allow us make new payment,
    cancel pyament and get the status of the payment request
    implementing the nequi api.
    """
    def __init__(self):
        """
        __Auth = attribute that will be instance with an Auth class
        """
        self.__Auth = None

    def new_payment(self, phone_number, value, reference_1=None):
        """
        request to make a new payment request with nequi api
        phone_nuber (str): number of th client that will make the payment
        value (int): value of money whothout decimals to pay
        reference_1 (str): optional data about transfer
        """
        new_payment = UnregisteredPaymentRequest(Auth=self.__Auth)
        return new_payment.create(
            phone_number=phone_number,
            value=value,
            reference_1=reference_1)

    def get_transaction_status(self, transaction_id, message_id):
        """
        request to get the status of a transaction
        transaction_id (str): id of the transacion, 
        (value returned in new_payment)
        message_id (str): is the id of the payment request,
        (also returned in new_payment).
        """
        status = GetStatusPayment(self.__Auth)
        return status.get_status(transaction_id, message_id)

    def cancel_transaction(self, phone_number, transaction_id, message_id):
        """
        request for cancellation of a payment request made
        phone_number (str): number on which the payment request was made
         transaction_id (str): id of the transacion, 
        (value returned in new_payment)
        message_id (str): is the id of the payment request,
        (also returned in new_payment).
        """
        new_cancel = CancelUnregisteredPaymentPush(Auth=self.__Auth)
        return new_cancel.cancel_payment(
            phone_number=phone_number,
            transaction_id=transaction_id,
            message_id=message_id
        )

    def Configuration(self, client_id, client_secret, api_key, auth_uri, grant_type,
                      api_base_path):
        """
        method to configure the Authentication credentials
        and gain access to the nequi api.
        """
        from ..authorization.auth import Auth

        credentials_config = CredentialsConfig(
            client_id=client_id,
            client_secret=client_secret,
            api_key=api_key,
            auth_uri=auth_uri,
            grant_type=grant_type,
            api_base_path=api_base_path,
        )
        self.__Auth = Auth(credentials_config)



if __name__ == "__main__":
    transaction = Transaction()
    """
    Get your credentials by registering at Nequi Conecta
    Link: https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjo2uDWt8_9AhViVTABHY6hBQAQFnoECA8QAQ&url=https%3A%2F%2Fconecta.nequi.com.co%2F&usg=AOvVaw1Vfy_Z_a-NlmAXKX2MUvGO
    """
    transaction.Configuration(
        client_id="Your client id here",
        client_secret="Your client secret here",
        api_key="api key here",
        auth_uri='https://oauth.sandbox.nequi.com/oauth2/token',
        grant_type='client_credentials',
        api_base_path='https://api.sandbox.nequi.com/')
    data = {}
    data = asyncio.run(transaction.new_payment(
            phone_number='number asigned by the nequi team',
            value="value of the transaction",
            reference_1="slight description is optional"
        ))
    print(data)
    status = asyncio.run(transaction.get_transaction_status(data['transaction_id'], data['message_id']))
    print(status)
    if (data):
        cancel = asyncio.run(transaction.cancel_transaction(phone_number=3400100156, transaction_id= data['transaction_id'], message_id= data['message_id']))
        print(cancel)

