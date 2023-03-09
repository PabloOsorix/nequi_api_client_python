from datetime import datetime
import requests_async as requests
import repackage
from ..errors import get_error

REST_REVERSE_END_POINT = 'payments/v2/-services-reverseservices-reversetransaction'

repackage.up()
class ReversePayment():
    """
    class to reverse a payment request implementing nequi api
    """
    def __init__(self, Auth) -> None:
        self.auth = Auth

    async def reversePayment(self, message_id, transaction_message_id, phone_number, value,):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': await self.auth.getToken(),
            'x-api-key': self.auth.Credentials.nequi_api_key()
        }
        url_end_point = f"{self.auth.Credentials.api_base_path}{REST_REVERSE_END_POINT}"

        data = {
            "RequestMessage": {
                "RequestHeader": {
                    "Channel": "PNP04-C001",
                    "RequestDate": (datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")),
                    "MessageID": f"{message_id}",
                    "ClientID": "12345",
                    "Destination": {
                        "ServiceName": "ReverseServices",
                        "ServiceOperation": "reverseTransaction",
                        "ServiceRegion": "C001",
                        "ServiceVersion": "1.0.0"
                    }
                },
                "RequestBody": {
                    "any": {
                        "reversionRQ": {
                            "phoneNumber": f"{phone_number}",
                            "value": f"{value}",
                            "code": "NIT_1",
                            "messageId": f"{transaction_message_id}",
                            "type": "payment"
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
                if (statusCode == 0 or statusCode == '0'):
                    return {
                            'statusDesc':'La transaccion ha sido reversada',
                            'statusCode': statusCode
                        }
                else:
                    error_msg = get_error(statusCode, statusDesc)
                    return {
                        'statusCode': statusCode,
                        'statusDesc': error_msg,
                    }
        except requests.exceptions.ConnectionError as err:
            return {'error': err}
        except requests.exceptions.HTTPError as err:
            return {'error': err}
        except requests.exceptions.RequestException as err:
            return {'error': err}