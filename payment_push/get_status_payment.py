from datetime import datetime
import requests_async as requests
from ..errors import get_error

REST_STATUS_END_POINT = "payments/v2/-services-paymentservice-getstatuspayment"


class GetStatusPayment():
    """
    Class to obtain the status of a payment request.
    """
    def __init__(self, Auth):
        self.status_code = {
            "33": "Pendiente",
            "34": "Cancelado o rechazado",
            "35": "Realizado",
            "69": "Caducada",
            "71": "Fallida"
        }
        self.auth = Auth

    async def get_status(self, transaction_id, message_id):

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': await self.auth.get_token(),
            'x-api-key': self.auth.Credentials.nequi_api_key()
        }

        url_endpoint = f"{self.auth.Credentials.api_base_path}{REST_STATUS_END_POINT}"

        data = {
            "RequestMessage": {
                "RequestHeader": {
                    "Channel": "PNP04-C001",
                    "RequestDate": (datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")),
                    "MessageID": f"{message_id}",
                    "ClientID": "12345",
                    "Destination": {
                        "ServiceName": "PaymentsService",
                        "ServiceOperation": "getStatusPayment",
                        "ServiceRegion": "C001",
                        "ServiceVersion": "1.0.0"
                    }
                },
                "RequestBody": {
                    "any": {
                        "getStatusPaymentRQ": {
                            "codeQR": f"{transaction_id}"
                        }
                    }
                }
            }
        }

        try:
            response = await requests.post(f"{url_endpoint}", headers=headers, json=data)
            if (response and response.status_code == 200):
                data = response.json()
                statusCode = data['ResponseMessage'].get('ResponseHeader').get('Status').get('StatusCode')
                statusDesc = data['ResponseMessage'].get('ResponseHeader').get('Status').get('StatusDesc')

                if statusCode == 0 or statusCode == '0':
                    status = data['ResponseMessage']['ResponseBody'].get('any').get(
                        'getStatusPaymentRS').get('status')
                    if status == '35':
                        return {
                            'statusCode': statusCode,
                            'statusDesc': self.status_code[status],
                            'status': status
                        }
                    else:
                        return {
                            'statusCode': statusCode,
                            'statusDesc': self.status_code[status],
                            'status': status
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