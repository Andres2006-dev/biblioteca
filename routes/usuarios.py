from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token,jwt_required
import uuid #generar un uid unico 
import re

usuarios_bp = Blueprint('usuarios', __name__)


#funcion para validar los correos
def correoValido(correo):
    patron = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return re.match(patron, correo) is not None
#-----------------

#funcion para validar la contraseña
def contraseniaValida(contrasenia):
    patron = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    return re.match(patron,contrasenia) is not None
#-----------------

@usuarios_bp.route('/login', methods=['POST'])
def login():
    
    if not request.is_json:
        return jsonify({"mensaje":"No se estan enviando datos en el cuerpo"}),400
    
    peticion = request.get_json()    
    
    if peticion  is None:
        return jsonify({"mensaje":"No se recibió información en el cuerpo de la petición"}),400
    
    campos_requeridos = ['correo','contrasenia']
    faltantes = [campo for campo in campos_requeridos if not peticion.get(campo) or str(peticion.get(campo)).strip()==""]
    
    if len(faltantes)>0:
        return jsonify({"mensaje":f"faltan campos en la peticion {faltantes}"}),400
    
    correo = peticion['correo'].strip()
    # if not correoValido(correo):
    #     return jsonify({"mensaje":"El correo ingresado es invalido"})
    contrasenia = peticion['contrasenia'].strip()

    try:
        con = current_app.mysql.connection.cursor()
        con.execute("SELECT * FROM t_usuarios WHERE correo=%s",[correo])
        current_app.mysql.connection.commit()
        usuario = con.fetchone()
        con.close()
        if not usuario:
            return jsonify({"mensaje":"El correo no está registrado"}),401
        
        if not check_password_hash(usuario[10],contrasenia):
            return jsonify({"mensaje": "La contraseña es incorrecta"}), 401
        
        acces_token = create_access_token(identity=correo)
        return jsonify({"mensaje":"Inicio de sesion exitoso",
                        "token"  :acces_token}),200
    except Exception as e:
        return jsonify({"mensaje":f"Error al iniciar sesion: {str(e)}"}),500
    
#ruta para listar los usuarios
@usuarios_bp.route('/', methods=['GET'])
# @jwt_required()
def listadoUsuarios():
    con = current_app.mysql.connection.cursor() #poder interacctuar con la db
    con.execute("SELECT * FROM t_usuarios WHERE estado = 1")
    usuarios = con.fetchall() #recupera todos los datos de la db 
    con.close()
    print("lista",usuarios)
    listado = []
    for usuario in usuarios:
        listado.append({"id":usuario[0],"uid":usuario[1],"primer_nombre":usuario[2], "segundo_nombre":usuario[3],
                        "primer_apellido":usuario[4], "segundo_apellido":usuario[5],
                        "estado":usuario[6],"correo":usuario[7],"telefono":usuario[8],"direccion":usuario[9]})
    return jsonify(listado)
#----------------

#ruta para registrar usuarios
@usuarios_bp.route('/', methods=['POST'])
# @jwt_required()
def registroUsuario():
    
    if not request.is_json:
        return jsonify({"mensaje":"No se estan enviando datos en el cuerpo"}),400
    
    
    peticion    = request.json
    if peticion  is None:
        return jsonify({"mensaje":"No se recibió información en el cuerpo de la petición"}),400

    campos_requeridos = ["primer_nombre", "primer_apellido", "correo", "telefono", "direccion","contrasenia"]
    #poder hacer una validacion mas fuerte por si no se envia el campo o por si se envia vacio
    faltantes = [x for x in campos_requeridos if not peticion.get(x) or str(peticion.get(x)).strip()==""] #el strip me quita los espacios en blanco

    if len(faltantes)>0:
        return jsonify({"mensaje":f"faltan campos en la peticion {faltantes}"})
    
    #guardar los datos que estan siendo enviados
    uid                  = uuid.uuid4() #generar un uid 
    pri_nombre           =peticion["primer_nombre"].strip()
    seg_nombre           =(peticion.get("segundo_nombre") or "").strip() or None
    pri_apellido         =peticion["primer_apellido"].strip()    
    seg_apellido         =(peticion.get("segundo_apellido") or "").strip() or None
    estado               = 1  #hacer que sea activo 
    correo               =peticion["correo"].strip()
    if not correoValido(correo):
        return jsonify({"mensaje": "El correo electrónico no es válido"}), 400
    
    con = current_app.mysql.connection.cursor()
    #validar que no exista un usuario con este correo
    con.execute("SELECT * FROM t_usuarios  WHERE correo =%s",[correo])
    usuario = con.fetchone()
    if usuario:
        return jsonify({"mensaje":"El correo electrónico ya está registrado"}),400
    
    telefono             =peticion["telefono"].strip()
    direccion            =peticion["direccion"].strip()
    contrasenia          =peticion["contrasenia"].strip()
    if not contraseniaValida(contrasenia):
        return jsonify({"mensaje":"La contraseña debe tener al menos 8 caracteres, incluir"
                                  "al menos una letra mayúscula, una letra minúscula, un número y un carácter especial"}),400
    contrasenia_encriptada = generate_password_hash(contrasenia)
    try: 
        con.execute("""
                INSERT INTO t_usuarios(uid,primer_nombre,segundo_nombre,primer_apellido,segundo_apellido,estado,correo,telefono,direccion,contrasenia)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """,[str(uid),pri_nombre,seg_nombre,pri_apellido,seg_apellido,estado,correo,telefono,direccion,contrasenia_encriptada])
        current_app.mysql.connection.commit() 
        con.close()   
        return jsonify({"mensaje":"Se ha registrado un usuario"})
    except Exception as e:
        return jsonify({"mensaje":f"Error al registrar el usuario y este es el error{str(e)}"}),500
#-----------

#editar usuario
@usuarios_bp.route('/<uid>', methods=['PUT'])
# @jwt_required()
def editarUsuario(uid):
    
    if not request.is_json:
        return jsonify({"mensaje":"No se estan enviando datos en el cuerpo"}),400
    
    peticion = request.json   
    if peticion  is None:
        return jsonify({"mensaje":"No se recibió información en el cuerpo de la petición"}),400  
    
    
    campos_requeridos = ["primer_nombre", "primer_apellido", "correo", "telefono", "direccion"]
    #poder hacer una validacion mas fuerte por si no se envia el campo o por si se envia vacio
    faltantes = [x for x in campos_requeridos if not peticion.get(x) or str(peticion.get(x)).strip()==""] #el strip me quita los espacios en blanco
    if len(faltantes)>0:
        return jsonify({"mensaje":f"faltan los campos en la peticion {faltantes}"})
    pri_nombre           =peticion["primer_nombre"].strip() 
    seg_nombre           =(peticion.get("segundo_nombre") or "").strip() or None
    pri_apellido         =peticion["primer_apellido"].strip()    
    seg_apellido         =(peticion.get("segundo_apellido")or "").strip() or None
    correo               =peticion["correo"].strip()
    #usar la funcion para verificar el correo
    if not correoValido(correo):
        return jsonify({"mensaje": "El correo electrónico no es válido"}), 400
    
    con = current_app.mysql.connection.cursor()
    #validar que no exista un mismo correo
    con.execute("SELECT * FROM t_usuarios WHERE correo=%s",[correo])
    usuario = con.fetchall()
    print("usuarios: ", usuario)
    if usuario and usuario[0][1]!=uid:
        return jsonify({"mensaje":"El correo electrónico ya está registrado"}),400
    #------------------ 
    telefono             =peticion["telefono"].strip()
    direccion            =peticion["direccion"].strip()

    try:
        con.execute("SELECT * FROM t_usuarios WHERE uid=%s",[uid])
        usuario = con.fetchone() #poder encontrar el primer resultado
        if usuario:
            con.execute(
                """
                UPDATE t_usuarios SET primer_nombre=%s,segundo_nombre=%s,primer_apellido=%s,
                segundo_apellido=%s,correo=%s,telefono=%s,direccion=%s WHERE uid = %s
                """,[pri_nombre,seg_nombre,pri_apellido,seg_apellido,correo,telefono,direccion,uid]
            )
            current_app.mysql.connection.commit()
            con.close()
            return jsonify({"mensaje":f"El usuario fue actualizado con exito"})
        else:
            return jsonify({"mensaje":"El usuario no fue encontrado"}),404

    except Exception as e:
        return jsonify({"mensaje":f"Error al actualizar el usuario: {str(e)}"}),500
#---------------

#eliminar usuario (cambiar de estado)
@usuarios_bp.route('/<uid>', methods=['DELETE'])
# @jwt_required()
def eliminarUsuario(uid):
    estado = 0
    try:
        con = current_app.mysql.connection.cursor()

        con.execute("SELECT * FROM t_usuarios WHERE uid=%s",[uid])
        usuario = con.fetchone() #poder encontrar el primer resultado

        if usuario: #validar de que el usuario si exista
            con.execute("""
                        UPDATE t_usuarios SET estado = %s WHERE uid = %s    
                        """,[estado,uid])
            current_app.mysql.connection.commit()
            con.close()
            return jsonify({"mensaje":f"El usuario fue eliminado con exito"})
        else:
            return jsonify({"mensaje":"No se encontro ningun usuario"}),404
    except Exception as e:
        return jsonify({"mensaje":f"Error al eliminar el usuario error: {str(e)}"}),500
#---------