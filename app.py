from flask import Flask,render_template,url_for,flash,redirect,request,session
from flask_uploads import configure_uploads,IMAGES,UploadSet
from time import time
import jwt
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash,check_password_hash

from forms import *
from db import *

app = Flask(__name__)


app.config.update(SECRET_KEY="la_llave")
app.config['UPLOADED_IMAGES_DEST']='static/img'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'inventariot3@gmail.com'
app.config['MAIL_PASSWORD'] = '&Inventario12'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail= Mail(app)

images=UploadSet('images',extensions=('jpg', 'jpe', 'jpeg', 'png'))
configure_uploads(app,images)

def esAdmin():
    return session.get("usuario").get("rol") == "Administrador"

def esVendor():
    return session.get("usuario").get("rol") == "Vendedor"

def usuarioLogeado():
    return session.get("usuario")

def obtener_token(id,expires_in=600):
    return jwt.encode({'reset_password':id,'exp':time()+expires_in},app.config["SECRET_KEY"],algorithm="HS256").decode('utf-8')

def enviar_correo(usuario):
    token=obtener_token(usuario[0][2])
    msg=Message('Recuperar contraseña del inventario',sender='inventariot3@gmail.com',recipients=[usuario[0][1]])
    #msg.body="Tu token es: "+url_for('reset',token=token,_external=True)
    msg.html=render_template('email.html',usuario=usuario[0][2],token=token)
    mail.send(msg)
    #send_email('')

def verificacion_token(token):
    try:
        id = jwt.decode(token, app.config['SECRET_KEY'],algorithms=['HS256'])['reset_password']
    except:
        return
    return id

@app.route("/",methods=['GET', 'POST'])
@app.route("/index",methods=['GET', 'POST'])
def index():
    form = FormularioLogin()
        
    if form.validate_on_submit():
        user = obtener_usuario(form.user.data)
        if user:
            validarContra = check_password_hash(user[0][3],form.password.data)
            if validarContra:
                session["usuario"] = {"nom_usuario":user[0][2],"rol":user[0][4]}
                return redirect(url_for("home"))
        else:
            flash("Usuario o Contraseña incorrectos.")
    return render_template("index.html",form=form)

@app.route("/home",methods=['GET', 'POST'])
def home():
    if not usuarioLogeado():
        return redirect("/index")

    usuario=FormularioNuevoUsuario()
    producto=FormularioNuevoProducto()
    actualizar=FormularioActualizarAdmin()
    todos=FormularioTodos()
    productos = get_productos()
    if request.method=="POST":
        if todos.validate_on_submit():
            if todos.todos.data:
                productos=get_all()
        if usuario.enviar.data and usuario.validate():
            insertar_usuario(usuario.name.data,usuario.email.data,usuario.user.data,generate_password_hash(usuario.password.data),usuario.rol.data)
            return redirect("/home")
        if producto.enviar2.data and producto.validate():
            try:
                if producto.imagen.data.filename!='':
                    insertar_producto(producto.referencia.data,producto.producto.data,producto.precio.data,producto.cantidad.data,producto.estado.data,producto.imagen.data)
                    filename=images.save(producto.imagen.data)
            except:
                insertar_producto(producto.referencia.data,producto.producto.data,producto.precio.data,producto.cantidad.data,producto.estado.data,'noimage.jpg')

            return redirect('/home')
        if actualizar.enviar3.data and actualizar.validate():
            actualizar_producto(actualizar.referencia.data,actualizar.producto.data,actualizar.precio.data,actualizar.cantidad.data,actualizar.estado.data,actualizar.imagen.data)
            try:
                if actualizar.imagen.data == "":
                    filename=images.save(actualizar.imagen.data)
            except:
                pass
            return redirect('/home')
    return render_template("home.html",form=usuario,form2=producto,form3=actualizar,productos = productos,form4=todos)

@app.route("/recuperar",methods=['GET', 'POST'])
def recuperar():
    if usuarioLogeado():
        return redirect("/home")
    form=FormularioRecuperar()
    if form.validate_on_submit():
        # Aca tengo que hacer query para encontrar el usuario dada un email
        usuario=obtener_usuario(form.correo.data) #No estoy seguro que necesite todo el usuario
        if usuario:
            enviar_correo(usuario)
        return redirect("/")
    return render_template("recuperar.html",form=form)

@app.route("/cerrar",methods=['GET','POST'])
def cerrarSesion():
    session.pop("usuario")
    flash("Sesión Cerrada.")
    return redirect("/index")


@app.route("/reset/<token>",methods=['GET','POST'])
def reset(token):
    if usuarioLogeado():
        return redirect(url_for('home'))
    usuario=verificacion_token(token)
    if not usuario:
        return redirect(url_for('index'))
    formulario=FormularioReseteo()
    if formulario.validate_on_submit():
        cambiar_password(generate_password_hash(formulario.contra.data),usuario)
        return redirect(url_for('index'))
    return render_template("reset.html",formulario=formulario)


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)


