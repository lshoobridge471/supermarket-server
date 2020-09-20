# Supermarket-HTTP-Server

Servidor web para obtener datos sobre productos de un supermercado.
Creado por Lucas Shoobridge.
Fecha: 2020-09-20

## Pasos a seguir para iniciar:
- Copiar/mover el archivo config.cfg.example a "config.cfg" y configurarlo a gusto.
- Parámetros a configurar:
    - bind_address: IP donde emitirá el servidor.
    - bind_port: PUERTO donde escuchará el servidor.
    - token: si se descomenta esta línea y se especifica, para cada request deberá pasar como el header "Authentication" especificando el Token que se especifique en el archivo config.
    - json_file: archivo desde donde leerá los datos del supermercado.

## Para levantar:
- Instalar los requirements.txt (usa python2).
- Ejecutar: python supermarket.py

Con eso se iniciará el servidor en IP/puerto indicados.

## Para realizar llamadas y obtener datos:
Para realizar llamadas y obtener datos de productos, debemos llamar al path: /get_products indicándole el query_param upc_list.
Nota: se pueden pasar muchos UPC separados por comas ','.

Ejemplo de llamadas:
- Simple: http://localhost:8000/get_products?upc_list=77912312341
- Múltiple: http://localhost:8000/get_products?upc_list=77912312341,53478734814,29349823748

Nota: No hay límite de UPC's a pasarle.

## Datos relevantes:

Lista de UPC para probar: 7794000003361,7798353430010,7798169802063,7791290788909,7790742034502,7793890255966,7792640000313,7792640000269,7790742344007,7798039850026,7793890251432,7790250015055,7792180001665,7793100111556,7790040994904,7790670051831

Si se pasa un UPC que no existe, directamete no se almacenará en el JSON de respuesta.