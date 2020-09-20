# -*- coding: UTF-8 -*-
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from pprint import pprint
import urlparse, json, ConfigParser
import traceback, sys

# Definimos el archivo de configuración.
_CONFIG_FILE = 'config.cfg'
# Levantamos archivo de configuración
config = ConfigParser.ConfigParser()
config.read(_CONFIG_FILE)

# Configuramos IP y puerto.
_SRV_ADDR = config.get("main","bind_address","localhost")
try:
    SRV_PORT = config.getint("main","bind_port")
except:
    SRV_PORT = 8000
    
# Verificamos si se definio un Token manual para poder acceder al server.
_AUTH_TOKEN = config.get("auth", "token", False)
# Archivo de datos
_DATA_FILE = config.get("data","json_file","data.json")

class API(BaseHTTPRequestHandler):
    """
        Clase que maneja las requests para un supermercado online.
        Lee un archivo JSON y devuelve los datos solicitados.
        Creada por: Lucas Shoobridge (@lshoobridge)
        Fecha: 2020-09-20
    """
    
    def do_GET(self):
        """
            Definimos el método GET.
        """
        # Obtenemos el path del request.
        path = urlparse.urlparse(self.path)
        # Almacenamos los datos de la llamada en una variable temporal.
        call_data = {
            'headers': self.headers, # Obtenemos los headers.
            'path_real': path.path, # Path llamado
            'path_query': path.query, # Path llamado
        }
        try:
            # Respuesta por defecto.
            ret = { "status": "ERR", "msg": "Ocurrio un error, por favor, intente nuevamente.", "data": {} }
            # Verificamos si la autenticación por Token está activada y si el Token pasado
            # en el header "Authentication" coincide.
            if _AUTH_TOKEN and not (call_data['headers'].get('Authentication', '') == _AUTH_TOKEN):
                ret['msg'] = 'Token de autenticación inválido.'
                # Devolvemos la respuesta
                self.send_response(401)
                # Devolvemos los headers.
                self.end_headers()
                # Devolvemos el contenido
                self.wfile.write(json.dumps(ret))
            else:
                # Verificamos el path al que accedió.
                if call_data['path_real'] == '/get_products':
                    """
                        Ejemplo a recibir de path_query:
                        call_data['path_query'] = 'upc_list=77912312341,53478734814,29349823748'
                    """
                    params = {} # Diccionario donde se almacenarán los parámetros.
                    products = {} # Diccionario donde se almacenarán los parámetros.
                    # Obtenemos los datos de los productos a los que quiere acceder
                    query_params = call_data.get('path_query', False)
                    # Si se obtuvieron.
                    if query_params:
                        # Hacemos split para separar todos los parámetros.
                        query_params = query_params.split('&')
                        # Recorremos los parámetros.
                        for param in query_params:
                            try:
                                # Obtenemos los datos del parámetro
                                key = param.split('=')[0] # Obtengo el nombre del parámetro
                                value = param.split('=')[1] # Obtengo el valor del parámetro
                                params[key] = value # Lo almacenamos en la variable de los parámetros.
                            except Exception as e:
                                print 'Error al procesar query param ({}): {}'.format(param, e)
                    # Si se pudieron procesar query_params, vamos a ver la lista de UPC
                    # que recibimos. Por el momento es el único parámetro que nos interesa.
                    if params.get('upc_list', False):
                        # Aquí procesamos los UPC.
                        upc_list = params.get('upc_list').split(',') # Los separamos por comas, en el caso que vengan muchos.
                        # Abrimos el archivo JSON donde están los datos del supermercado.
                        with open(_DATA_FILE) as json_file:
                            try:
                                file_data = json.load(json_file)
                                # Recorremos los UPC obtenidos.
                                for upc in upc_list:
                                    try:
                                        # Obtenemos el valor del UPC.
                                        products[upc] = file_data[upc]
                                    except Exception as e:
                                        print 'Error al procesar UPC {}: {}'.format(upc, e)
                            except Exception as e:
                                print 'Error al procesar el archivo "{}": {}'.format(_DATA_FILE, e)
                    # Almacenamos los datos en la respuestas JSON.
                    ret['data'] = products
                    ret['msg'] = 'Los datos fueron obtenidos con éxito.'
                    ret['status'] = 'OK'
                    # Devolvemos la respuesta
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(ret))
                else:
                    # Devolvemos la respuesta
                    self.send_response(404)
                    # Devolvemos los headers.
                    self.end_headers()
                    # Devolvemos el contenido
                    self.wfile.write("Page not found!")
        except:
            # Devolvemos la respuesta
            self.send_response(500)
            # Devolvemos los headers.
            self.end_headers()
            # Devolvemos el contenido
            self.wfile.write("Page error!")
        return

if __name__ == '__main__':
    try:
        server = HTTPServer((_SRV_ADDR, SRV_PORT), API)
        print 'Starting server at http://{}:{}'.format(_SRV_ADDR, SRV_PORT)
        server.serve_forever()
    except Exception as e:
        print 'Error at starting server: {}'.format(e)
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60