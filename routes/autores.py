from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
import uuid #generar un uid unico 

autores_bp = Blueprint('autores', __name__)

#ruta para listar los autores
@autores_bp.route('/', methods=['GET'])
# @jwt_required()
def listadoAutores():
    con = current_app.mysql.connection.cursor() #poder interacctuar con la db
    con.execute("SELECT * FROM t_autores WHERE aut_estado = 1")
    autores = con.fetchall() #recupera todos los datos de la db 
    print("lista",autores)
    listado = []
    for autor in autores:
        listado.append({"id":autor[0],"uid":autor[1],"aut_nombre":autor[2], "aut_estado":autor[3]})
    return jsonify(listado)
#--------------------------

#ruta para registar los autores
@autores_bp.route('/', methods=['POST'])
# @jwt_required()
def registrarAutor():
    
    if not request.is_json:
        return jsonify({"mensaje":"No se estan enviando datos en el cuerpo"}),400
    
    peticion    = request.json
    if peticion  is None:
        return jsonify({"mensaje":"No se recibió información en el cuerpo de la petición"}),400  

    campos_requeridos = ["aut_nombre"]
    #poder hacer una validacion mas fuerte por si no se envia el campo o por si se envia vacio
    faltantes = [x for x in campos_requeridos if not peticion.get(x) or str(peticion.get(x)).strip()==""] #el strip me quita los espacios en blanco
    if len(faltantes)>0:
        return jsonify({"mensaje":f"faltan campos en la peticion {faltantes}"})
    
    #guardar los datos que estan siendo enviados
    uid                  = uuid.uuid4() #generar un uid 
    aut_nombre           =peticion["aut_nombre"].strip()   
    aut_estado           =1 #actvo 

    con = current_app.mysql.connection.cursor()
    #validar que no exista un autor con ese nombre
    con.execute("SELECT * FROM t_autores  WHERE aut_nombre = %s",[aut_nombre])
    autores = con.fetchone()
    if autores:
        return jsonify({"mensaje":"Ya existe un autor con este nombre"})

    try:
        
        con.execute("""
                INSERT INTO t_autores(aut_uid, aut_nombre, aut_estado)
                VALUES(%s,%s,%s)
                """,[uid, aut_nombre, aut_estado])
        current_app.mysql.connection.commit() 
        con.close()

        return jsonify({"mensaje":"Se ha registrado un autor"})
    except Exception as e:
        return jsonify({"mensaje":f"Error al registrar el autor y este es el error{str(e)}"})
    
#------------------------------------------------


#ruta para editar los autores
@autores_bp.route('/<uid>', methods=['PUT'])
# @jwt_required()
def editarAutor(uid):
    
    if not request.is_json:
        return jsonify({"mensaje":"No se estan enviando datos en el cuerpo"}),400
    
    peticion    = request.json
    if peticion  is None:
        return jsonify({"mensaje":"No se recibió información en el cuerpo de la petición"}),400  

    campos_requeridos = ["aut_nombre"]
    #poder hacer una validacion mas fuerte por si no se envia el campo o por si se envia vacio
    faltantes = [x for x in campos_requeridos if not peticion.get(x) or str(peticion.get(x)).strip()==""] #el strip me quita los espacios en blanco
    if len(faltantes)>0:
        return jsonify({"mensaje":f"faltan campos en la peticion {faltantes}"})
    
    #guardar los datos que estan siendo enviados
    aut_nombre           =peticion["aut_nombre"].strip() 
    
    con = current_app.mysql.connection.cursor()
    #validar que no exista un autor con ese nombre
    con.execute("SELECT * FROM t_autores  WHERE aut_nombre = %s",[aut_nombre])
    autores = con.fetchall()
    if autores and autores[0][1]!=uid:
        return jsonify({"mensaje":"Ya existe un autor con este nombre"})

    try:
        con.execute("SELECT * FROM t_autores WHERE aut_uid=%s",[uid])
        autores = con.fetchone() #poder encontrar el primer resultado
        if autores:
            con.execute(
                """
                UPDATE t_autores SET  aut_nombre=%s WHERE aut_uid=%s
                """,[ aut_nombre, uid]
            )
            current_app.mysql.connection.commit()
            con.close()
            return jsonify({"mensaje":f"el autor fue actualizado con exito"})
        else:
            return jsonify({"mensaje":"El autor no se encontro"}),404

    except Exception as e:
        return jsonify({"mensaje":f"Error al actualizar el autor: {str(e)}"}),500
    #-----------------------------------------------


#ruta para eliminar autores 
@autores_bp.route('/<uid>', methods=['DELETE'])
# @jwt_required()
def eliminarAutor(uid):
    aut_estado = 0
    try:
        con = current_app.mysql.connection.cursor()

        con.execute("SELECT * FROM t_autores WHERE aut_uid=%s",[uid])
        autores = con.fetchone() #poder encontrar el primer resultado

        if autores: #validar de que el usuario si exista
            con.execute("""
                        UPDATE t_autores SET aut_estado =%s WHERE aut_uid =%s    
                        """,[aut_estado,uid])
            current_app.mysql.connection.commit()
            con.close()
            return jsonify({"mensaje":f"el autor fue eliminado con exito"})
        else:
            return jsonify({"mensaje":"No se encontro ningun autor"}),404
    except Exception as e:
        return jsonify({"mensaje":f"Error al eliminar al autor: {str(e)}"})

#--------------------------