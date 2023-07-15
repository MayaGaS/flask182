from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

#inicialización del servidor Flask
app= Flask(__name__)
app.config['MYSQL_HOST']= "localhost"
app.config['MYSQL_USER']= "root"
app.config['MYSQL_PASSWORD']= ""
app.config['MYSQL_DB']= "DB_Floreria"

app.secret_key = 'mysecretkey'

mysql = MySQL(app)

#--- Declaración de rutas ---

# Ruta index o ruta principal http://localhost:5000
# La ruta se compone de nombre y función

@app.route('/')
def index():
    curSelect = mysql.connection.cursor()
    curSelect.execute('select * from tbFlores')
    consulta = curSelect.fetchall()
    #print(consulta)    
    
    return render_template('index.html', listtbFlores = consulta) 



@app.route('/guardar', methods=['POST'])
def guardar():
    if request.method == 'POST':
        Vnombre= request.form['txtNombre']
        Vcantidad= request.form['txtCantidad']
        Vprecio= request.form['txtPrecio']

        CS = mysql.connection.cursor()
        CS.execute('insert into tbFlores(nombre, cantidad, precio) values(%s, %s, %s)', (Vnombre, Vcantidad, Vprecio))
        mysql.connection.commit()
        
    flash('Flor Agregada Correctamente')
    return redirect(url_for('index'))


@app.route('/editar/<id>')
def editar(id):
    curEditar = mysql.connection.cursor()
    curEditar.execute('select * from tbFlores where id = %s', (id,))
    consulId = curEditar.fetchone()

    return render_template('editarFlor.html', album = consulId)


@app.route('/actualizar/<id>', methods=['POST'])
def actualizar(id):
    if request.method=='POST':
        Vnombre= request.form['txtNombre']
        Vcantidad= request.form['txtCantidad']
        Vprecio= request.form['txtPrecio']

        curAct = mysql.connection.cursor()
        curAct.execute('update tbFlores set nombre = %s, cantidad = %s, precio = %s where id = %s', (Vnombre, Vcantidad, Vprecio, id))
        mysql.connection.commit()

    flash('Flor Actualizada Correctamente')
    return redirect(url_for('index'))

# Ejecución de servidor
if __name__== '__main__':
    app.run(port= 5000, debug=True)