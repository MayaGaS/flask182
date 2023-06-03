import tkinter as tk
from tkinter import ttk
import mysql.connector

# Establecer la conexión con la base de datos
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    database="bebidas"
)

# Crear el cursor para ejecutar las consultas
cursor = conexion.cursor()

def mostrar_registros():
    # Consultar los datos de la tabla Bebidas con los nombres de clasificación y marca asociados
    consulta = """
    SELECT b.id, b.Nombre, b.Precio, c.clasificacion, m.Marca
    FROM Bebidas b
    JOIN Clasificaciones c ON b.id_clasificacion = c.id
    JOIN Marca m ON b.id_marca = m.id
    """
    cursor.execute(consulta)
    bebidas = cursor.fetchall()

    # Crear un widget Treeview para mostrar los registros en una tabla
    tabla_registros = ttk.Treeview(pestaña_mostrar, columns=("ID", "Nombre", "Precio", "Clasificación", "Marca"), show="headings")

    # Configurar las columnas de la tabla
    tabla_registros.heading("ID", text="ID")
    tabla_registros.heading("Nombre", text="Nombre")
    tabla_registros.heading("Precio", text="Precio")
    tabla_registros.heading("Clasificación", text="Clasificación")
    tabla_registros.heading("Marca", text="Marca")

    # Mostrar los datos obtenidos en la tabla
    for bebida in bebidas:
        tabla_registros.insert("", tk.END, values=(bebida[0], bebida[1], bebida[2], bebida[3], bebida[4]))

    tabla_registros.pack(fill="both", expand=True)

def agregar_registro():
    # Crear etiquetas y campos de entrada para los datos del nuevo registro
    etiqueta_nombre = tk.Label(pestaña_agregar, text="Nombre:")
    etiqueta_nombre.pack()
    campo_nombre = tk.Entry(pestaña_agregar)
    campo_nombre.pack()

    etiqueta_precio = tk.Label(pestaña_agregar, text="Precio:")
    etiqueta_precio.pack()
    campo_precio = tk.Entry(pestaña_agregar)
    campo_precio.pack()

    etiqueta_id_clasificacion = tk.Label(pestaña_agregar, text="ID Clasificación:")
    etiqueta_id_clasificacion.pack()
    campo_id_clasificacion = tk.Entry(pestaña_agregar)
    campo_id_clasificacion.pack()

    etiqueta_id_marca = tk.Label(pestaña_agregar, text="ID Marca:")
    etiqueta_id_marca.pack()
    campo_id_marca = tk.Entry(pestaña_agregar)
    campo_id_marca.pack()
    
    def agregar():
        nombre = campo_nombre.get()
        precio = campo_precio.get()
        id_clasificacion = campo_id_clasificacion.get()
        id_marca = campo_id_marca.get()

        # Insertar un nuevo registro en la tabla Bebidas
        consulta = f"INSERT INTO Bebidas (Nombre, Precio, id_clasificacion, id_marca) VALUES ('{nombre}', {precio}, {id_clasificacion}, {id_marca})"
        cursor.execute(consulta)
        conexion.commit()
        print("Registro agregado correctamente.")

        campo_nombre.delete(0, tk.END)
        campo_precio.delete(0, tk.END)
        campo_id_clasificacion.delete(0, tk.END)
        campo_id_marca.delete(0, tk.END)

    boton_agregar = tk.Button(pestaña_agregar, text="Agregar", command=agregar)
    boton_agregar.pack()


def eliminar_registro():
    # Crear etiqueta y campo de entrada para el ID del registro a eliminar
    etiqueta_id = tk.Label(pestaña_eliminar, text="ID del registro a eliminar:")
    etiqueta_id.pack()
    campo_id = tk.Entry(pestaña_eliminar)
    campo_id.pack()

    # Función para eliminar el registro de la base de datos
    def eliminar():
        id_registro = campo_id.get()

        # Eliminar el registro de la tabla Bebidas
        consulta = f"DELETE FROM Bebidas WHERE id = {id_registro}"
        cursor.execute(consulta)
        conexion.commit()
        print("Registro eliminado correctamente.")

        campo_id.delete(0, tk.END)

    boton_eliminar = tk.Button(pestaña_eliminar, text="Eliminar", command=eliminar)
    boton_eliminar.pack()

def actualizar_registro():
    # Crear etiquetas y campos de entrada para el ID del registro a editar y los nuevos campos
    etiqueta_id = tk.Label(pestaña_actualizar, text="ID del registro a editar:")
    etiqueta_id.pack()
    campo_id = tk.Entry(pestaña_actualizar)
    campo_id.pack()

    etiqueta_nuevo_nombre = tk.Label(pestaña_actualizar, text="Nuevo nombre:")
    etiqueta_nuevo_nombre.pack()
    campo_nuevo_nombre = tk.Entry(pestaña_actualizar)
    campo_nuevo_nombre.pack()

    etiqueta_nuevo_precio = tk.Label(pestaña_actualizar, text="Nuevo precio:")
    etiqueta_nuevo_precio.pack()
    campo_nuevo_precio = tk.Entry(pestaña_actualizar)
    campo_nuevo_precio.pack()

    etiqueta_nueva_clasificacion = tk.Label(pestaña_actualizar, text="Nueva clasificación:")
    etiqueta_nueva_clasificacion.pack()
    campo_nueva_clasificacion = tk.Entry(pestaña_actualizar)
    campo_nueva_clasificacion.pack()

    etiqueta_nueva_marca = tk.Label(pestaña_actualizar, text="Nueva marca:")
    etiqueta_nueva_marca.pack()
    campo_nueva_marca = tk.Entry(pestaña_actualizar)
    campo_nueva_marca.pack()

    # Función para editar el registro en la base de datos
    def actualizar():
        id_registro = campo_id.get()
        nuevo_nombre = campo_nuevo_nombre.get()
        nuevo_precio = campo_nuevo_precio.get()
        nueva_clasificacion = campo_nueva_clasificacion.get()
        nueva_marca = campo_nueva_marca.get()

        # Actualizar los campos del registro en la tabla Bebidas
        consulta = f"UPDATE Bebidas SET Nombre='{nuevo_nombre}', Precio={nuevo_precio}, id_clasificacion={nueva_clasificacion}, id_marca={nueva_marca} WHERE id={id_registro}"
        cursor.execute(consulta)
        conexion.commit()
        print("Registro editado correctamente.")

        campo_id.delete(0, tk.END)
        campo_nuevo_nombre.delete(0, tk.END)
        campo_nuevo_precio.delete(0, tk.END)
        campo_nueva_clasificacion.delete(0, tk.END)
        campo_nueva_marca.delete(0, tk.END)

    boton_actualizar = tk.Button(pestaña_actualizar, text="Actualizar", command=actualizar)
    boton_actualizar.pack()

#Función para obtener el precio promedio
def calcular_precio_promedio():
    # Consultar el precio promedio de las bebidas
    consulta1 = "SELECT AVG(Precio) FROM Bebidas"
    cursor.execute(consulta1)
    resultado = cursor.fetchone()[0]

    # Mostrar el resultado en una etiqueta
    etiqueta_resultado.config(text=f"Precio promedio de las bebidas: {resultado}")

    # Consultar la cantidad de bebidas por marca
    consulta2 = """
    SELECT m.Marca, COUNT(*) AS Cantidad
    FROM Bebidas b
    JOIN Marca m ON b.id_marca = m.id
    GROUP BY m.Marca
    """
    cursor.execute(consulta2)
    resultados = cursor.fetchall()

    # Mostrar los resultados en una tabla
    tabla_resultados.delete(*tabla_resultados.get_children())

    for resultado in resultados:
        tabla_resultados.insert("", tk.END, values=(resultado[0], resultado[1]))

    # Consultar la cantidad de bebidas por clasificación
    consulta3 = """
    SELECT c.clasificacion, COUNT(*) AS Cantidad
    FROM Bebidas b
    JOIN Clasificaciones c ON b.id_clasificacion = c.id
    GROUP BY c.clasificacion
    """
    cursor.execute(consulta3)
    resultados = cursor.fetchall()

    # Mostrar los resultados en una tabla
    tabla_resultados.delete(*tabla_resultados.get_children())

    for resultado in resultados:
        tabla_resultados.insert("", tk.END, values=(resultado[0], resultado[1]))
    
  

# Crear la ventana principal
ventana_principal = tk.Tk()
ventana_principal.title("Interfaz de Bebidas")
ventana_principal.geometry("600x300")

# Crear el widget Notebook
pestañas = ttk.Notebook(ventana_principal)

# Crear las pestañas
pestaña_mostrar = ttk.Frame(pestañas)
pestaña_agregar = ttk.Frame(pestañas)
pestaña_eliminar = ttk.Frame(pestañas)
pestaña_actualizar = ttk.Frame(pestañas)
pestaña_mostrar_calculos = ttk.Frame(pestañas)

# Agregar las pestañas al widget Notebook
pestañas.add(pestaña_mostrar, text="Mostrar registros")
pestañas.add(pestaña_agregar, text="Agregar registro")
pestañas.add(pestaña_eliminar, text="Eliminar registro")
pestañas.add(pestaña_actualizar, text="Actualizar registro")

# Configurar el relleno de las pestañas
pestañas.pack(expand=1, fill="both", padx=10, pady=10)

# Agregar contenido a cada pestaña
mostrar_registros()
agregar_registro()
eliminar_registro()
actualizar_registro()

# Ejecutar la interfaz
ventana_principal.mainloop()

# Cerrar el cursor y la conexión
cursor.close()
conexion.close()