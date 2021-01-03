import sqlite3
from sqlite3 import Error

def sql_connection():
    try:
        con = sqlite3.connect('Inventario.db')
        return con
    except Error:
        print(Error)

def consultar_producto(nombre):
    query = "SELECT * FROM Producto WHERE nombre = ?;"
    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute(query,(nombre))
    con.commit()
    producto = cursorObj.fetchall()
    con.close()
    return producto

def get_productos():
    query = "SELECT * FROM Producto WHERE estado=1;"
    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute(query)
    con.commit()
    productos = cursorObj.fetchall()
    con.close()
    return productos

def get_all():
    query = "SELECT * FROM Producto ORDER BY estado DESC;"
    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute(query)
    con.commit()
    productos = cursorObj.fetchall()
    con.close()
    return productos

def insertar_producto(referencia,nombre,precio,cantidad,estado,imagen):
    try:
        resimagen='../static/img/'+imagen.filename
    except:
        resimagen='../static/img/'+imagen
    query = "INSERT INTO Producto (referencia,nombre,precio,cantidad,estado,imagen) values(?,?,?,?,?,?)" 
    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute(query,(referencia,nombre,precio,cantidad,estado,resimagen))
    con.commit()
    con.close()

def actualizar_producto(referencia,nombre,precio,cantidad,estado,imagen):
    tprecio=str(precio)
    tcantidad=str(cantidad)
    try:
        if imagen.filename!='':
            resimagen='../static/img/'+imagen.filename
            query = "UPDATE Producto SET referencia = ?, nombre = ?, precio = ?, cantidad = ?,estado=?, imagen = ? WHERE referencia = ?;"
            con = sql_connection()
            cursorObj = con.cursor()
            cursorObj.execute(query,(referencia,nombre,tprecio,tcantidad,estado,resimagen,referencia))
            con.commit()
            con.close()  

    except:
        query = "UPDATE Producto SET referencia = ?, nombre = ?, precio = ?, cantidad = ?, estado=? WHERE referencia = ?;"  
        con = sql_connection()
        cursorObj = con.cursor()
        cursorObj.execute(query,(referencia,nombre,tprecio,tcantidad,estado,referencia))
        con.commit()
        con.close()   
         
     

def insertar_usuario(nombre,correo,usuario,password,rol):
    query = "INSERT INTO USUARIO (nombre,correo,usuario,password,rol) values(?,?,?,?,?);"
    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute(query,(nombre,correo,usuario,password,rol))
    con.commit()
    con.close()

def obtener_usuario(email):
    query="SELECT * FROM Usuario WHERE correo = ?"
    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute(query,[email])
    con.commit()
    usuario = cursorObj.fetchall()
    con.close()
    return usuario

def validar_usuario(usuario):
    query = "SELECT * FROM Usuario WHERE usuario = ?;"
    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute(query,[usuario])
    con.commit()
    usuario = cursorObj.fetchall()
    con.close()
    return usuario

def validar_password(usuario,password):
    query = "SELECT * FROM Usuario WHERE usuario = ? and password = ?;"
    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute(query,(str(usuario),str(password)))
    con.commit()
    rs = cursorObj.fetchall()
    con.close()
    return rs

def get_usuarios():
    query = "SELECT nombre,rol FROM Usuario;"
    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute(query)
    con.commit()
    rs = cursorObj.fetchall()
    con.close()
    return rs

def cambiar_password(password,usuario):
    query = "UPDATE Usuario SET password = ?  WHERE usuario = ?;"  
    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute(query,(password,usuario))
    con.commit()
    con.close()
