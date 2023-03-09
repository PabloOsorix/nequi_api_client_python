#Nequi-api errors found in:
#https://docs.conecta.nequi.com.co/?api=unregisteredPayments#!/Pagos32con32Push/post_services_paymentservice_unregisteredpayment

errors = {
    "2-CCSB000012": "La cuenta del usuario se encuentra bloqueada",
    "2-CCSB000013": "La cuenta del usuario se encuentra bloqueada",
    "2-CCSB000079": "No se encontro un dato en el core financiero, puede que la transaccion o messageId no exista",
    "3-451": "Cliente o usuario no encontrado en base de datos",
    "3-455": "Resgistro no encontrado en base de datos",
    "10-454": "La transacción ha expirado",
    "10-455": "La transacción ha sido cancelada o rechazada",
    "11-9L": "El phoneNumber, code o transactionId no existen",
    "11-17L": "Error de formato/parseo en alguno de los atributos del request",
    "11-18L": "Timeout en el componente de logica de negocio",
    "11-37L": "La cuenta de un usuario no existe",
    "20-05A ":"Cuando se hace una petición pero en el body vienen parametros incorrectos",
    "20-07A": "Error técnico en Lambda",
    "20-08A ":"Dato no encontrado en repositorio o en dynamoDB",
    }

def get_error(statusCode, statusDesc):
    if errors[statusCode]:
        return errors[statusCode]
    return statusDesc