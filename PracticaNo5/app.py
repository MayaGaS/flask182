
from flask import Flask

#Inicializacion del servidor Flask
app = Flask(__name__)

#Configuracion para la conexion a BD
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = " "
app.config['MYSQL_DB'] = "dbflask"


#Declaracion de rutas


#Ruta Index http://localhost:5000
#La rurta se compone de nombre y funcion 
@app.route('/')
def index():
    return "Hola Mundo"

@app.route('/guardar')
def guardar():
    return "Se guardo el album en la BD"

@app.route('/eliminar')
def eliminar():
    return "Se elimino el album en la BD"


#Ejecucion de servidor 
if __name__ == '__main__':
    app.run(port = 5000, debug = True) 