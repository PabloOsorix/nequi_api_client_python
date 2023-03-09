import requests_async as requests
from datetime import datetime
from uuid import uuid4
from ..errors import get_error
REST_PAYMENT_END_POINT = "payments/v2/-services-paymentservice-unregisteredpayment"


class UnregisteredPaymentRequest():
    """
    Class that make a new request payment implementing the nequi-api
    """
    def __init__(self, Auth):
        self.auth = Auth

    async def create(self, phone_number, value, reference_1=None):

        message_id = str(uuid4())[:33]
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': await self.auth.get_token(),
            'x-api-key': self.auth.Credentials.nequi_api_key()
        }
        end_point = f"{self.auth.Credentials.api_base_path}{REST_PAYMENT_END_POINT}"

        data = {
            "RequestMessage": {
                "RequestHeader": {
                    "Channel": "PNP04-C001",
                    # datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
                    "RequestDate": (datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")),
                    "MessageID": f"{message_id}",
                    "ClientID": "12345",  # authConfig.transaction_client_id
                    "Destination": {
                        "ServiceName": "PaymentsService",
                        "ServiceOperation": "unregisteredPayment",
                        "ServiceRegion": "C001",
                        "ServiceVersion": "1.2.0"
                    }
                },
                "RequestBody": {
                    "any": {
                        "unregisteredPaymentRQ": {
                            "phoneNumber": f"{phone_number}",
                            "code": "NIT_1",  # type and number of ID of the commerce who realize de charge
                            # amount to colled, haven't thousand separators
                            "value": f"{value}",
                            # optional field to save additional transaction info
                            "reference1": f"{reference_1}",
                            "reference2": "reference2",
                            "reference3": "reference3"
                        }
                    }
                }
            }
        }

        try:
            response = await requests.post(f'{end_point}', headers=headers, json=data)

            if (response and response.status_code == 200):
                data = response.json()
                statusCode = data['ResponseMessage'].get(
                    'ResponseHeader').get('Status').get('StatusCode')
                statusDesc = data['ResponseMessage'].get(
                    'ResponseHeader').get('Status').get('StatusDesc')
                if (statusCode == 0 or statusCode == '0'):
                    transactionId = data['ResponseMessage']['ResponseBody']['any'].get(
                        'unregisteredPaymentRS').get('transactionId').strip()

                    return {
                        'statusCode': statusCode,
                        'statusDesc': 'Solicitud de pago realizada correctamente',
                        'transaction_id': transactionId,
                        'message_id': message_id
                    }
                else:
                    error_msg = get_error(statusCode, statusDesc)
                    return {
                            'statusCode': statusCode,
                            'statusDesc' : error_msg,
                        }
                        
        except requests.exceptions.ConnectionError as err:
            return {'error': err}
        except requests.exceptions.HTTPError as err:
            return {'error': err}
        except requests.exceptions.RequestException as err:
            return {'error': err}
