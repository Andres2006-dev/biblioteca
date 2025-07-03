from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
import uuid #generar un uid unico 

categoria_bp = Blueprint('categorias', __name__)


#ruta para listar categoria
@categoria_bp.route('/', methods=['GET'])
@jwt_required()
def listadoCategoria():
    con = current_app.mysql.connection.cursor() #poder interacctuar con la db
    con.execute("SELECT * FROM t_categorias WHERE cat_estado = 1")
    categorias = con.fetchall() #recupera todos los datos de la db 
    print("lista",categorias)
    listado = []
    for categoria in categorias:
        listado.append({"id":categoria[0],"uid":categoria[1],"cat_tipo":categoria[2], "cat_estado":categoria[3]})
    return jsonify(listado)
#-------------------------------------

#ruta para registrar categoria
@categoria_bp.route('/', methods=['POST'])
@jwt_required()
def registrarCategoria():
    
    if not request.is_json:
        return jsonify({"mensaje":"No se estan enviando datos en el cuerpo"}),400
    
    peticion    = request.get_json()
    if peticion  is None:
        return jsonify({"mensaje":"No se recibió información en el cuerpo de la petición"}),400  
    
    
    campos_requeridos = ["cat_tipo"]
    #poder hacer una validacion mas fuerte por si no se envia el campo o por si se envia vacio
    faltantes = [x for x in campos_requeridos if not peticion.get(x) or str(peticion.get(x)).strip()==""] #el strip me quita los espacios en blanco

    if len(faltantes)>0:
        return jsonify({"mensaje":f"faltan campos en la peticion {faltantes}"})
    
    #guardar los datos que estan siendo enviados
    uid                  = uuid.uuid4() #generar un uid 
    cat_tipo           =peticion["cat_tipo"].strip()  
    cat_estado           =1 #actvo 

    con = current_app.mysql.connection.cursor()
    #validar que no exista una categoria con ese nombre
    con.execute("SELECT * FROM t_categorias  WHERE cat_tipo = %s",[cat_tipo])
    categoria = con.fetchone()
    if categoria:
        return jsonify({"mensaje":"Ya existe una categoria con este nombre"})

    try:
        con.execute("""
                INSERT INTO t_categorias(cat_uid,cat_tipo,cat_estado)
                VALUES(%s,%s,%s)
                """,[uid,cat_tipo,cat_estado])
        current_app.mysql.connection.commit()
        con.close()    
        return jsonify({"mensaje":"Se ha registrado una categoria"})
    except Exception as e:
        return jsonify({"mensaje":f"Error al registrar la categoria y este es el error{str(e)}"}),500
#-------------------------------------


#ruta para editar categoria
@categoria_bp.route('/<uid>', methods=['PUT'])
@jwt_required()
def editarCategoria(uid):
    
    if not request.is_json:
        return jsonify({"mensaje":"No se estan enviando datos en el cuerpo"}),400
    
    peticion    = request.json
    if peticion  is None:
        return jsonify({"mensaje":"No se recibió información en el cuerpo de la petición"}),400  

    campos_requeridos = ["cat_tipo"]
    #poder hacer una validacion mas fuerte por si no se envia el campo o por si se envia vacio
    faltantes = [x for x in campos_requeridos if not peticion.get(x) or str(peticion.get(x)).strip()==""] #el strip me quita los espacios en blanco

    if len(faltantes)>0:
        return jsonify({"mensaje":f"faltan campos en la peticion {faltantes}"})
    
    #guardar los datos que estan siendo enviados
    cat_tipo           =peticion["cat_tipo"].strip() 
    
    con = current_app.mysql.connection.cursor()
    #validar que no exista una categoria con ese nombre
    con.execute("SELECT * FROM t_categorias  WHERE cat_tipo = %s",[cat_tipo])
    categoria = con.fetchall()
    if categoria and categoria[0][1]!=uid:
        return jsonify({"mensaje":"Ya existe una categoria con este nombre"}) 
    try:
        con.execute("SELECT * FROM t_categorias WHERE cat_uid=%s",[uid])
        categoria = con.fetchone() #poder encontrar el primer resultado
        if categoria:
            con.execute(
                """
                UPDATE t_categorias SET cat_tipo=%s WHERE cat_uid=%s
                """,[cat_tipo, uid]
            )
            current_app.mysql.connection.commit()
            con.close()
            return jsonify({"mensaje":f"La categoria fue actualizada con exito"})
        else:
            return jsonify({"mensaje":"El tipo de categoria no se encontro"}),404

    except Exception as e:
        return jsonify({"mensaje":f"Error al actualizar la categoria: {str(e)}"}),500
#------------------------------------------


#ruta par6a eliminar categoria
@categoria_bp.route('/<uid>', methods=['DELETE'])
@jwt_required()
def eliminarCategoria(uid):
    cat_estado = 0
    try:
        con = current_app.mysql.connection.cursor()

        con.execute("SELECT * FROM t_categorias WHERE cat_uid =%s",[uid])
        categoria = con.fetchone() #poder encontrar el primer resultado

        if categoria: #validar de que el usuario si exista
            con.execute("""
                        UPDATE t_categorias SET cat_estado = %s WHERE cat_uid =%s    
                        """,[cat_estado,uid])
            current_app.mysql.connection.commit()
            con.close()
            return jsonify({"mensaje":f"la categoria fue eliminada con exito"})
        else:
            return jsonify({"mensaje":"No se encontro ninguna categoria"}),404  
    except Exception as e:
        return jsonify({"mensaje":f"Error al eliminar la categoria: {str(e)}"}),500
