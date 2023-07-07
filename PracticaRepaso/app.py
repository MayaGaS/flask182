from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

#inicialización del servidor Flask
app= Flask(__name__)
app.config['MYSQL_HOST']= "localhost"
app.config['MYSQL_USER']= "root"
app.config['MYSQL_PASSWORD']= ""
app.config['MYSQL_DB']= "DB_Fruteria"

app.secret_key = 'mysecretkey'

mysql = MySQL(app)

#--- Declaración de rutas ---

# Ruta index o ruta principal http://localhost:5000
# La ruta se compone de nombre y función

@app.route('/')
def index():
    curSelect = mysql.connection.cursor()
    curSelect.execute('select * from tbFrutas')
    consulta = curSelect.fetchall()
    #print(consulta)    
    
    return render_template('index.html', listFrutas = consulta) 



@app.route('/guardar', methods=['POST'])
def guardar():
    if request.method == 'POST':
        Vfruta= request.form['txtFruta']
        Vtemporada= request.form['txtTemporada']
        Vprecio= request.form['txtPrecio']
        Vstock= request.form['txtStock']
        # print(titulo, artista, anio)

        CS = mysql.connection.cursor()
        CS.execute('insert into tbFrutas(fruta, temporada, precio, stock) values(%s, %s, %s, %s)', (Vfruta, Vtemporada, Vprecio, Vstock))
        mysql.connection.commit()
        
    flash('Album Agregado Correctamente')
    return redirect(url_for('index'))


@app.route('/editar/<id>')
def editar(id):
    curEditar = mysql.connection.cursor()
    curEditar.execute('select * from tbFrutas where id = %s', (id,))
    consulId = curEditar.fetchone()

    return render_template('editarAlbum.html', album = consulId)


@app.route('/actualizar/<id>', methods=['POST'])
def actualizar(id):
    if request.method=='POST':
        Vfruta= request.form['txtFruta']
        Vtemporada= request.form['txtTemporada']
        Vprecio= request.form['txtPrecio']
        Vstock= request.form['txtStock']

        curAct = mysql.connection.cursor()
        curAct.execute('update tbFrutas set fruta = %s, temporada = %s, precio = %s, stocktitulo = %s where id = %s', (Vfruta, Vtemporada, Vprecio, Vstock, id))
        mysql.connection.commit()

    flash('Fruta Actualizada Correctamente')
    return redirect(url_for('index'))


#-- ELIMINAR --
@app.route('/eliminar/<id>')
def eliminar(id):
    curEliminar = mysql.connection.cursor()
    curEliminar.execute('select * from tbFrutas where id = %s', (id,))
    consulId = curEliminar.fetchone()

    return render_template('eliminarFruta.html', album = consulId)

@app.route('/borrar/<id>', methods = ['POST'])
def borrar(id):
    curBorrar = mysql.connection.cursor()
    curBorrar.execute('delete from tbFrutas where id = %s', (id,))
    mysql.connection.commit()

    flash('Fruta Eliminada Correctamente')

    return redirect(url_for('index'))


# Ejecución de servidor
if __name__== '__main__':
    app.run(port= 5000, debug=True)