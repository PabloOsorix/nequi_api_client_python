from datetime import datetime
import requests_async as requests
from ..errors import get_error

REST_CANCEL_END_POINT = "payments/v2/-services-paymentservice-cancelunregisteredpayment"


class CancelUnregisteredPaymentPush():
    """
    Class to cancel a payment request implementing the nequi api
    """
    def __init__(self, Auth):
        """
        (Auth) = Auth class find in Authorization module, it is
        compose for a Credentials class find in CredentialsConfig
        module
        """
        self.auth = Auth

    async def cancel_payment(self, phone_number, transaction_id, message_id):
        
        headers = {
            'Content-Type': "application/json",
            'Accept': "application/json",
            'Authorization': await self.auth.get_token(),
            'x-api-key': self.auth.Credentials.nequi_api_key()
        }

        url_end_point = f"{self.auth.Credentials.api_base_path}{REST_CANCEL_END_POINT}"

        data = {
            "RequestMessage": {
                "RequestHeader": {
                    "Channel": "PNP04-C001",
                    "RequestDate": (datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")),
                    "MessageID": f"{message_id}",
                    "ClientID": "12345",
                    "Destination": {
                        "ServiceName": "PaymentsService",
                        "ServiceOperation": "unregisteredPayment",
                        "ServiceRegion": "C001",
                        "ServiceVersion": "1.0.0"
                    }
                },
                "RequestBody": {
                    "any": {
                        "cancelUnregisteredPaymentRQ": {
                            "code": "1",
                            "phoneNumber": f"{phone_number}",
                            "transactionId": f"{transaction_id}"
                        }
                    }
                }
            }
        }


        try:
            response = await requests.post(f"{url_end_point}", headers=headers, json=data)

            if (response and response.status_code == 200):
                data = response.json()
                statusCode = data['ResponseMessage'].get(
                    'ResponseHeader').get('Status').get('StatusCode')
                statusDesc = data['ResponseMessage'].get(
                    'ResponseHeader').get('Status').get('StatusDesc')
                if statusCode == 0 or statusCode == '0':
                    return {
                        "statusCode": statusCode,
                        "statusDesc": "Transaccion cancelada con exito"
                    }
                else:
                    error_msg = get_error(statusCode, statusDesc)
                    return {
                        'statusCode': statusCode,
                        'statusDesc': error_msg
                    }
        except requests.exceptions.ConnectionError as err:
            return {'error': err}
        except requests.exceptions.HTTPError as err:
            return {'error': err}
        except requests.exceptions.RequestException as err:
            return {'error': err}