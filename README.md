# nequi-api-client-python
Repositorio oficial de Nequi: https://github.com/nequibc

## Ejemplo para el consumo del API de Nequi en Python

El propósito de este ejemplo es ilustrativo para aquellos interesados en la integración con la API de Nequi
. Con este ejemplo podrá consumir el recurso de pagos con notificación ofrecidos por la API, y si lo desea podrá utilizar este código como base para el consumo del resto de recursos expuestos en la API. Para más información visite el portal para desarrolladores https://conecta.nequi.com.co.


## 1. Credenciales 
Debe registrarse en Nequi conecta para obtener:    
- Client Id    
- Client Secret    
- API Key

Los anteriores datos los podrá encontrar en la sección Credenciales en el siguiente enlace https://conecta.nequi.com/content/consultas.

## 2. Configuración
A diferencia del repositorio oficial de nequi, he realizado una clase llamada CredentialsConfig, se encuentra en el archivo `/authorization/credentials_config`, al ser una clase, debe instanciarse con las credenciales ya mencionadas.

### Librería 'request_async'

Todos los ejemplos aquí proporcionados usan la librería request_async para hacer el consumo de los endpoints.

## 3. Ejemplos de integracion

En el archivo encontrado en `/payment_push/transaction.py` encontrará la clase `Transaction()` 
en la cual decidí usar la composición de las demás clases para facilitar y centralizar el uso de estas, esta tendra
el atributo `self.__Auth` el cual será instanciado con la clase `Auth()` encontrada
en `/authorization/auth.py`esta a su vez se encontrara compuesta por la clase `CredentialsConfig` con el motivo de facilitar el acceso de las demás clases a las credenciales.

### Pagos Push 
En el archivo encontrado en `/payment_push/transaction/` podrá encontrar el código para:    
    - Solicitar un pago con notificación push.    
    - Cancelar una solicitud de pago realizada por notificación push    
    - Obtener el estado de una solicitud de pago realizada por notificación push.

## 4. Ejecutar los ejemplos
En la última sección del archivo  `/payment_push/transaction.py` se encuentra un ejemplo donde deberá reemplazar los espacios por sus credenciales, luego ejecutar el archivo con el comando `python3 transaction.py`.

