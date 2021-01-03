from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,SelectField,IntegerField,validators,BooleanField
from wtforms.fields.html5 import EmailField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import ValidationError

#PasswordField

class FormularioLogin(FlaskForm):
    user = EmailField('Usuario', [validators.DataRequired(message="Por favor completa con el correo"),validators.Email(message="Correo no valido")])
    password = PasswordField('Contraseña', [validators.DataRequired(message='Por favor completa con la contraseña')])
    enviar = SubmitField('Iniciar Sesión')

class FormularioRecuperar(FlaskForm):
    correo=EmailField('Correo',[validators.DataRequired(message="Por favor completa con el correo"),validators.Email(message="Correo no valido")])
    enviar=SubmitField('Recuperar contraseña')

class FormularioNuevoUsuario(FlaskForm):
    user = StringField('Usuario', [validators.DataRequired(message="Por favor completa con un usuario")])
    email= EmailField('Correo Electrónico',[validators.DataRequired(message="Por favor completa con un correo"),validators.Email(message="Correo no valido")])
    name= StringField('Nombre')
    password=PasswordField('Contraseña',[
        validators.DataRequired(message="Por favor completa con una contraseña"),
        validators.EqualTo('confirm',message="Contraseñas deben ser iguales"),
        validators.length(min=6,message="Longitud minima de 6 caracteres"),
        validators.regexp(regex=".*[A-Z]",message="Debe tener minimo una mayuscula"),
        validators.regexp(regex=".*[0-9]",message="Debe tener minimo un numero") 
    ])
    confirm=PasswordField('Confirmar contraseña',[
        validators.DataRequired(message="Por favor completa con la contraseña del campo anterior")
    ])
    rol=SelectField('Rol',choices=[('Administrador','Administrador'),('Vendedor','Vendedor')])
    enviar=SubmitField('Registrar')

class FormularioTodos(FlaskForm):
    todos=BooleanField('Todos')

class FormularioNuevoProducto(FlaskForm):
    referencia=StringField('Referencia',[validators.DataRequired(message="Por favor completa con la referencia del producto")])
    producto=StringField('Producto',[validators.DataRequired(message="Por favor completa con el nombre del producto")])
    cantidad=StringField('Cantidad')
    precio=StringField('Precio')
    estado=BooleanField('Estado',default="checked")
    imagen=FileField('Imagen',validators=[
        FileAllowed(['jpg', 'jpe', 'jpeg', 'png'], 'Solo se aceptan imagenes')
    ])
    enviar2=SubmitField('Crear producto')
    def validate_precio(form,field):
        try:
            res=int(field.data)
        except Exception:
            raise ValidationError('Precio no valido')

        if res<0:
            raise ValidationError("Costo del producto no puede ser negativo")

    def validate_cantidad(form,field):
        try:
            res=int(field.data)
        except Exception:
            raise ValidationError('Cantidad no valida')

        if res<1:
            raise ValidationError("Minimo debe haber un producto")

class FormularioActualizarAdmin(FlaskForm):
    referencia=StringField('Referencia',[validators.DataRequired(message="Por favor completa con la referencia del producto")])
    producto=StringField('Producto',[validators.DataRequired(message="Por favor completa con el nombre del producto")])
    cantidad=StringField('Cantidad')
    precio=StringField('Precio')
    estado=BooleanField('Estado',default="checked")
    imagen=FileField('Imagen')
    enviar3=SubmitField('Actualizar')

    def validate_precio(form,field):
        try:
            res=int(field.data)
        except Exception:
            raise ValidationError('Precio no valido')

        if res<0:
            raise ValidationError("Costo del producto no puede ser negativo")

    def validate_cantidad(form,field):
        try:
            res=int(field.data)
        except Exception:
            raise ValidationError('Cantidad no valida')

        if res<1:
            raise ValidationError("Minimo debe haber un producto")





class FormularioReseteo(FlaskForm):
    contra = PasswordField('Contraseña',[
        validators.DataRequired(message="Por favor completa con una contraseña"),
        validators.EqualTo('contra2',message="Contraseñas deben ser iguales"),
        validators.length(min=6,message="Longitud minima de 6 caracteres"),
        validators.regexp(regex=".*[A-Z]",message="Debe tener minimo una mayuscula"),
        validators.regexp(regex=".*[0-9]",message="Debe tener minimo un numero") 
    ])
    contra2 = PasswordField('Repetir contraseña', [
        validators.DataRequired(message="Por favor escriba la contraseña del campo anterior")
    ])
    submit = SubmitField('Cambiar contraseña')