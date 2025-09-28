"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from src.api.models import db, Users, Clientes, Envios, Categorias, Productos, Promociones, VariantesProductos, Reviews, Favoritos, Ventas, DetallesVentas, Pagos
from src.api.utils import generate_sitemap, APIException, admin_required
from flask_cors import CORS
from decimal import Decimal
from sqlalchemy import select

users_bp = Blueprint('users_bp', __name__)
clients_bp = Blueprint('clients_bp', __name__)


# Allow CORS requests to this API
CORS(users_bp)
CORS(clients_bp)

#rutas para USERS ADMIN
#listar Todos los usuarios
@users_bp.route('/users', methods=['GET'])
@jwt_required()
@admin_required
def get_users():
    stmt= select(Users)
    users = db.session.execute(stmt).scalars().all()
    response_body = [user.serialize() for user in users]
    return jsonify(response_body), 200

#Usuar by id
@users_bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
@admin_required
def get_user(user_id):
    stmt= select(Users).where(Users.id==user_id)
    user = db.session.execute(stmt).scalar_one_or_none()
    if not user:
       return jsonify({"error": "Usuario no encontrado"}), 404
    return jsonify(user.serialize()), 200

#actualizar
@users_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_user(user_id):
    user = Users.query.get(user_id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    data = request.json
    if "email" in data:
        user.email = data["email"]
    if "password" in data:
        user.set_password(data["password"])
    if "rol" in data:
        user.rol = data["rol"]

    db.session.commit()
    return jsonify(user.serialize()), 200

#eliminar
@users_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_user(user_id):
    user = Users.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Usuario eliminado"}), 200

#Endpoints para Categorias
@users_bp.route('/categorias', methods=['GET'])
@jwt_required()
@admin_required
def get_all_categorias():
    stmt = select(Categorias)
    categorias = db.session.execute(stmt).scalars().all()
    response_body = [cat.serialize() for cat in categorias]
    return jsonify(response_body), 200

@users_bp.route('/categorias/<int:categoria_id>', methods=['GET'])
@jwt_required()
@admin_required
def get_one_categoria(categoria_id):
    stmt = select(Categorias).where(Categorias.id == categoria_id)
    categoria = db.session.execute(stmt).scalar_one_or_none()
    if not categoria:
        return jsonify({"Error": "Categoria no encontrada"}), 404
    return jsonify(categoria.serialize()), 200

@users_bp.route('/categorias', methods=['POST'])
@jwt_required()
@admin_required
def create_categoria():
    data = request.get_json()
    if not data.get("nombre") or not data.get("descripcion"):
        return jsonify({"error": "Nombre y descripción requeridos"}), 400
    categoria = Categorias(
        nombre = data["nombre"],
        descripcion = data["descripcion"]
    )
    db.session.add(categoria)
    db.session.commit()
    return jsonify(categoria.serialize()), 201

@users_bp.route('/categorias/<int:categoria_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_categoria(categoria_id):
    data = request.get_json()

    stmt = select(Categorias).where(Categorias.id == categoria_id)
    categoria = db.session.execute(stmt).scalar_one_or_none()

    if not categoria:
        return jsonify({"error": "Categoría no encontrada"}), 404

    categoria.nombre = data.get("nombre", categoria.nombre)
    categoria.descripcion = data.get("descripcion", categoria.descripcion)

    db.session.commit()
    return jsonify(categoria.serialize()), 200

@users_bp.route('/categorias/<int:categoria_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_categoria(categoria_id):
    stmt = select(Categorias).where(Categorias.id == categoria_id)
    categoria = db.session.execute(stmt).scalar_one_or_none()

    if not categoria:
        return jsonify({"error": "Categoría no encontrada"}), 404

    db.session.delete(categoria)
    db.session.commit()

    return jsonify({"msg": "Categoría eliminada correctamente"}), 200
#Endpoints Productos
@users_bp.route('/productos', methods=['GET'])
@jwt_required()
@admin_required
def get_productos():
    stmt= select(Productos)
    productos = db.session.execute(stmt).scalars().all()
    response = [p.serialize() for p in productos]
    return jsonify(response), 200

@users_bp.route('/productos/<int:producto_id>', methods=['GET'])
@jwt_required()
@admin_required
def get_one_producto(producto_id):
    stmt = select(Productos).where(Productos.id == producto_id)
    producto = db.session.execute(stmt).scalar_one_or_none()
    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404
    return jsonify(producto.serialize()), 200

@users_bp.route('/productos', methods=['POST'])
@jwt_required()
@admin_required
def create_producto():
    data= request.get_json()
    required_fields = ["nombre", "id_categoria", "descripcion", "imagen_url"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Todos los campos son obligatorios"}), 404
    #Verifica que la categoria exista
    stmt = select(Categorias).where(Categorias.id == data["id_categoria"])
    categoria = db.session.execute(stmt).scalar_one_or_none()
    if not categoria:
        return jsonify({"error": "Categoría no encontrada"}), 404
    producto = Productos(
        nombre=data["nombre"],
        id_categoria=data["id_categoria"],
        descripcion=data["descripcion"],
        imagen_url=data["imagen_url"],
        activo=data.get("activo", True)
    )
    db.session.add(producto)
    db.session.commit()
    return jsonify(producto.serialize()), 201

@users_bp.route('/productos/<int:producto_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_producto(producto_id):
    data= request.get_json()
    stmt = select(Productos).where(Productos.id == producto_id)
    producto = db.session.execute(stmt).scalar_one_or_none()
    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404
    #Si se quiere cambiar de categoría, validar que exista
    if "id_categoria" in data:
        stmt_cat= select(Categorias).where(Categorias.id == data["id_categoria"])
        categoria = db.session.execute(stmt_cat).scalar_one_or_none()
        if not categoria:
            return jsonify({"error": "Categoría no encontrada"}), 404
    producto.nombre=data.get("nombre", producto.nombre)
    producto.id_categoria=data.get("id_categoria", producto.id_categoria)
    producto.descripcion= data.get("descripcion", producto.descripcion)
    producto.imagen_url = data.get("imagen_url", producto.imagen_url)
    producto.activo = data.get("activo", producto.activo)
    db.session.commit()
    return jsonify(producto.serialize()), 200

@users_bp.route('/productos/<int:producto_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_producto(producto_id):
    stmt = select(Productos).where(Productos.id == producto_id)
    producto = db.session.execute(stmt).scalar_one_or_none()
    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404
    db.session.delete(producto)
    db.session.commit()
    return jsonify({"msg": "Producto eliminado correctamente"}), 200

#Variante Producto
@users_bp.route('/productos/<int:producto_id>/variantes', methods=['GET'])
@jwt_required()
@admin_required
def get_variantes_by_producto(producto_id):
    stmt = select(VariantesProductos).where(VariantesProductos.id_producto == producto_id)
    variantes = db.session.execute(stmt).scalars().all()
    return jsonify([v.serialize() for v in variantes]), 200

@users_bp.route('/variantes/<int:variante_id>', methods=['GET'])
@jwt_required()
@admin_required
def get_variante(variante_id):
    stmt = select(VariantesProductos).where(VariantesProductos.id == variante_id)
    variante = db.session.execute(stmt).scalar_one_or_none()
    if not variante:
        return jsonify({"error": "Variante no encontrada"}), 404
    return jsonify(variante.serialize()), 200

@users_bp.route('/productos/<int:producto_id>/variantes', methods=['POST'])
@jwt_required()
@admin_required
def create_variante(producto_id):
    data = request.get_json()
    required_fields = ["atributo", "valor", "precio", "stock"]
    missing = [f for f in required_fields if not data.get(f)]
    if missing:
        return jsonify({"error": f"Faltan campos obligatorios: {', '.join(missing)}"}), 400

    # Verificar que el producto exista
    stmt = select(Productos).where(Productos.id == producto_id)
    producto = db.session.execute(stmt).scalar_one_or_none()
    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404

    variante = VariantesProductos(
        id_producto=producto_id,
        atributo=data["atributo"],
        valor=data["valor"],
        precio=data["precio"],
        stock=data["stock"],
        activo=data.get("activo", True)
    )
    db.session.add(variante)
    db.session.commit()
    return jsonify(variante.serialize()), 201

@users_bp.route('/variantes/<int:variante_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_variante(variante_id):
    data = request.get_json()
    stmt = select(VariantesProductos).where(VariantesProductos.id == variante_id)
    variante = db.session.execute(stmt).scalar_one_or_none()

    if not variante:
        return jsonify({"error": "Variante no encontrada"}), 404
    # Actualizar solo si vienen en el body
    variante.atributo = data.get("atributo", variante.atributo)
    variante.valor = data.get("valor", variante.valor)
    variante.precio = data.get("precio", variante.precio)
    variante.stock = data.get("stock", variante.stock)
    variante.activo = data.get("activo", variante.activo)
    db.session.commit()
    return jsonify(variante.serialize()), 200

@users_bp.route('/variantes/<int:variante_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_variante(variante_id):
    stmt = select(VariantesProductos).where(VariantesProductos.id == variante_id)
    variante = db.session.execute(stmt).scalar_one_or_none()

    if not variante:
        return jsonify({"error": "Variante no encontrada"}), 404
    db.session.delete(variante)
    db.session.commit()
    return jsonify({"msg": "Variante eliminada correctamente"}), 200

# Endpoints para Promociones
@users_bp.route('/promociones', methods=['GET'])
@jwt_required()
@admin_required
def get_promociones():
    stmt = select(Promociones)
    promociones = db.session.execute(stmt).scalars().all()
    return jsonify([p.serialize() for p in promociones]), 200

@users_bp.route('/promociones/<int:promo_id>', methods=['GET'])
@jwt_required()
@admin_required
def get_promocion(promo_id):
    stmt = select(Promociones).where(Promociones.id == promo_id)
    promo = db.session.execute(stmt).scalar_one_or_none()
    if not promo:
        return jsonify({"error": "Promoción no encontrada"}), 404
    return jsonify(promo.serialize()), 200

@users_bp.route('/promociones', methods=['POST'])
@jwt_required()
@admin_required
def create_promocion():
    data = request.get_json()
    required_fields = ["codigo_promocional", "descuento_porcentaje", "fecha_inicio", "fecha_fin"]
    missing = [f for f in required_fields if not data.get(f)]
    if missing:
        return jsonify({"error": f"Faltan campos obligatorios: {', '.join(missing)}"}), 400
    # Verificar que no exista el código
    if Promociones.query.filter_by(codigo_promocional=data["codigo_promocional"]).first():
        return jsonify({"error": "El código promocional ya existe"}), 409
    promo = Promociones(
        codigo_promocional=data["codigo_promocional"],
        descuento_porcentaje=data["descuento_porcentaje"],
        fecha_inicio=datetime.fromisoformat(data["fecha_inicio"]),
        fecha_fin=datetime.fromisoformat(data["fecha_fin"]),
        activo=data.get("activo", True)
    )
    db.session.add(promo)
    db.session.commit()
    return jsonify(promo.serialize()), 201

@users_bp.route('/promociones/<int:promo_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_promocion(promo_id):
    data = request.get_json()
    stmt = select(Promociones).where(Promociones.id == promo_id)
    promo = db.session.execute(stmt).scalar_one_or_none()
    if not promo:
        return jsonify({"error": "Promoción no encontrada"}), 404
    promo.codigo_promocional = data.get("codigo_promocional", promo.codigo_promocional)
    promo.descuento_porcentaje = data.get("descuento_porcentaje", promo.descuento_porcentaje)
    if "fecha_inicio" in data:
        promo.fecha_inicio = datetime.fromisoformat(data["fecha_inicio"])
    if "fecha_fin" in data:
        promo.fecha_fin = datetime.fromisoformat(data["fecha_fin"])
    promo.activo = data.get("activo", promo.activo)
    db.session.commit()
    return jsonify(promo.serialize()), 200

@users_bp.route('/promociones/<int:promo_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_promocion(promo_id):
    stmt = select(Promociones).where(Promociones.id == promo_id)
    promo = db.session.execute(stmt).scalar_one_or_none()
    if not promo:
        return jsonify({"error": "Promoción no encontrada"}), 404
    db.session.delete(promo)
    db.session.commit()
    return jsonify({"msg": "Promoción eliminada correctamente"}), 200

@users_bp.route('/ventas', methods=['GET'])
@jwt_required()
@admin_required
def get_ventas():
    stmt = select(Ventas)
    ventas = db.session.execute(stmt).scalars().all()
    return jsonify([v.serialize() for v in ventas]), 200

@users_bp.route('/ventas/<int:venta_id>', methods=['GET'])
@jwt_required()
@admin_required
def get_venta_admin(venta_id):
    stmt = select(Ventas).where(Ventas.id == venta_id)
    venta = db.session.execute(stmt).scalar_one_or_none()
    if not venta:
        return jsonify({"error": "Venta no encontrada"}), 404
    return jsonify(venta.serialize()), 200

@users_bp.route('/ventas/<int:venta_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_venta_admin(venta_id):
    data = request.get_json()
    stmt = select(Ventas).where(Ventas.id == venta_id)
    venta = db.session.execute(stmt).scalar_one_or_none()
    if not venta:
        return jsonify({"error": "Venta no encontrada"}), 404
    if "estado_envio" in data:
        venta.estado_envio = data["estado_envio"]
    if "numero_seguimiento" in data:
        venta.numero_seguimiento = data["numero_seguimiento"]
    db.session.commit()
    return jsonify(venta.serialize()), 200

@users_bp.route('/ventas/<int:venta_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_venta_admin(venta_id):
    stmt = select(Ventas).where(Ventas.id == venta_id)
    venta = db.session.execute(stmt).scalar_one_or_none()
    if not venta:
        return jsonify({"error": "Venta no encontrada"}), 404
    db.session.delete(venta)
    db.session.commit()
    return jsonify({"msg": "Venta eliminada correctamente"}), 200

@users_bp.route('/ventas/<int:venta_id>/detalles', methods=['GET'])
@jwt_required()
@admin_required
def get_detalles_venta_admin(venta_id):
    stmt = select(DetallesVentas).where(DetallesVentas.id_venta == venta_id)
    detalles = db.session.execute(stmt).scalars().all()
    return jsonify([d.serialize() for d in detalles]), 200

@users_bp.route('/ventas/<int:venta_id>/detalles/<int:detalle_id>', methods=['GET'])
@jwt_required()
@admin_required
def get_detalle_venta_admin(venta_id, detalle_id):
    stmt = select(DetallesVentas).where(
        DetallesVentas.id == detalle_id,
        DetallesVentas.id_venta == venta_id
    )
    detalle = db.session.execute(stmt).scalar_one_or_none()
    if not detalle:
        return jsonify({"error": "Detalle no encontrado"}), 404
    return jsonify(detalle.serialize()), 200

@users_bp.route('/reviews', methods=['GET'])
@jwt_required()
@admin_required
def get_all_reviews():
    stmt = select(Reviews)
    reviews = db.session.execute(stmt).scalars().all()
    return jsonify([r.serialize() for r in reviews]), 200

@users_bp.route('/reviews/<int:review_id>', methods=['GET'])
@jwt_required()
@admin_required
def get_review_admin(review_id):
    review = db.session.get(Reviews, review_id)
    if not review:
        return jsonify({"error": "Review no encontrada"}), 404
    return jsonify(review.serialize()), 200

@users_bp.route('/reviews/<int:review_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_review_admin(review_id):
    review = db.session.get(Reviews, review_id)
    if not review:
        return jsonify({"error": "Review no encontrada"}), 404
    db.session.delete(review)
    db.session.commit()
    return jsonify({"msg": "Review eliminada correctamente"}), 200

@users_bp.route('/pagos', methods=['GET'])
@jwt_required()
@admin_required
def get_all_pagos():
    stmt = select(Pagos)
    pagos = db.session.execute(stmt).scalars().all()
    return jsonify([p.serialize() for p in pagos]), 200

@users_bp.route('/pagos/<int:pago_id>', methods=['GET'])
@jwt_required()
@admin_required
def get_pago_admin(pago_id):
    pago = db.session.get(Pagos, pago_id)
    if not pago:
        return jsonify({"error": "Pago no encontrado"}), 404
    return jsonify(pago.serialize()), 200

@users_bp.route('/pagos/<int:pago_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_pago_admin(pago_id):
    data = request.get_json()
    pago = db.session.get(Pagos, pago_id)
    if not pago:
        return jsonify({"error": "Pago no encontrado"}), 404
    # Solo permitir actualizar estado y detalles
    pago.estado = data.get("estado", pago.estado)
    pago.detalles = data.get("detalles", pago.detalles)
    db.session.commit()
    return jsonify(pago.serialize()), 200
    
#Enpoints para USERS clientes
@clients_bp.route('/clientes', methods=['GET'])
@jwt_required()
def get_client():
    user_id = get_jwt_identity()
    cliente = Clientes.query.filter_by(user_id=user_id).first_or_404()
    return jsonify(cliente.serialize()), 200

@clients_bp.route('/clientes/<int:cliente_id>', methods=['GET'])
@jwt_required()
def get_client_by_id(cliente_id):
    cliente = Clientes.query.get_or_404(cliente_id)
    return jsonify(cliente.serialize()), 200

@clients_bp.route('/registro', methods=['POST'])
def register_client():
    data = request.json
    if not data.get("email") or not data.get("password"):
        return jsonify({"error": "Email y contraseña requeridos"}), 400
    if Users.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Usuario ya existe"}), 409
    new_user = Users(email=data["email"])
    new_user.set_password(data["password"])
    db.session.add(new_user)
    db.session.commit()
    access_token = create_access_token(identity=new_user.id)
    return jsonify({"token": access_token, "user": new_user.serialize()}), 201

@clients_bp.route('/login', methods=['POST'])
def login_client():
    data = request.json
    user = Users.query.filter_by(email=data.get("email")).first()
    if not user or not user.check_password(data.get("password")):
        return jsonify({"error": "Credenciales inválidas"}), 401
    access_token = create_access_token(identity=user.id)
    return jsonify({"token": access_token, "user": user.serialize()}), 200

@clients_bp.route('/perfil', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = Users.query.get(user_id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    cliente = Clientes.query.filter_by(user_id=user.id).first()
    return jsonify({
        "user": user.serialize(),
        "cliente": cliente.serialize() if cliente else None
    }), 200

@clients_bp.route('/perfil', methods=['POST'])
@jwt_required()
def create_profile():
    user_id = get_jwt_identity()
    data = request.json
    # Verificar si ya existe perfil
    if Clientes.query.filter_by(user_id=user_id).first():
        return jsonify({"error": "Perfil ya existe"}), 400
    # Validar campos obligatorios
    required_fields = ["tipo_documento", "documento_identidad", "nombre", 
                       "apellido_paterno", "apellido_materno", "telefono"]
    missing = [f for f in required_fields if not data.get(f)]
    if missing:
        return jsonify({"error": f"Faltan campos obligatorios: {', '.join(missing)}"}), 400
    cliente = Clientes(
        user_id=user_id,
        tipo_documento=data["tipo_documento"],
        documento_identidad=data["documento_identidad"],
        nombre=data["nombre"],
        apellido_paterno=data["apellido_paterno"],
        apellido_materno=data["apellido_materno"],
        telefono=data["telefono"],
        genero=data.get("genero"),
        fecha_nacimiento=data.get("fecha_nacimiento"),
        avatar_url=data.get("avatar_url")
    )
    db.session.add(cliente)
    db.session.commit()
    return jsonify(cliente.serialize()), 201

@clients_bp.route('/perfil', methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    data = request.json
    cliente = Clientes.query.filter_by(user_id=user_id).first()
    if not cliente:
        return jsonify({"error": "No existe perfil, primero debes crearlo"}), 404
    # Campos que sí puede actualizar
    updatable_fields = [
        "tipo_documento", "documento_identidad", "nombre", 
        "apellido_paterno", "apellido_materno", "telefono",
        "genero", "fecha_nacimiento", "avatar_url"
    ]
    # Actualizar solo los que vengan en la petición
    for field in updatable_fields:
        if field in data:
            setattr(cliente, field, data[field])
    db.session.commit()
    return jsonify(cliente.serialize()), 200

@clients_bp.route('/clientes/<int:cliente_id>', methods=['DELETE'])
@jwt_required()
def delete_client(cliente_id):
    user_id = get_jwt_identity()
    user = Users.query.get(user_id)
    cliente = Clientes.query.get_or_404(cliente_id)
    if user.rol == "admin":
        db.session.delete(cliente)
        db.session.commit()
        return jsonify({"message": "Cliente eliminado por admin"}), 200
    if cliente.user_id != user_id:
        return jsonify({"error": "No tienes permiso para eliminar este perfil"}), 403
    db.session.delete(cliente)
    db.session.commit()
    return jsonify({"message": "Cliente eliminado"}), 200

@clients_bp.route('/envios', methods=['GET'])
@jwt_required()
def get_all_envios():
    user_id = get_jwt_identity()
    stmt= select(Envios).where(Envios.cliente_id == user_id)
    envios = db.session.execute(stmt).scalars().all()
    response_body = [envio.serialize() for envio in envios]
    return jsonify(response_body), 200

@clients_bp.route('/envios/<int:id>', methods=['GET'])
@jwt_required()
def get_one_envio(id):
    user_id = get_jwt_identity()
    stmt = select(Envios).where(Envios.id == id, Envios.cliente_id == user_id)
    envio = db.session.execute(stmt).scalar_one_or_none()
    if not envio:
       return jsonify({"error": "Envío no encontrado"}), 404
    return jsonify(envio.serialize()), 200

@clients_bp.route('/envios', methods=['POST'])
@jwt_required()
def create_envio():
    #Crear una nueva dirección de envío
    user_id = get_jwt_identity()
    data = request.get_json()
    required_fields = ["pais", "provincia", "ciudad", "direccion", "codigo_postal", "telefono_contacto"]
    missing = [f for f in required_fields if not data.get(f)]
    if missing:
        return jsonify({"error": f"Faltan campos: {', '.join(missing)}"}), 400
    envio = Envios(
        cliente_id=user_id,
        pais=data["pais"],
        provincia=data["provincia"],
        ciudad=data["ciudad"],
        direccion=data["direccion"],
        codigo_postal=data["codigo_postal"],
        telefono_contacto=data["telefono_contacto"]
    )
    db.session.add(envio)
    db.session.commit()
    return jsonify(envio.serialize()), 201

@clients_bp.route('/envios/<int:envio_id>', methods=['PUT'])
@jwt_required()
def update_envio(envio_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    stmt = select(Envios).where(
        Envios.id == envio_id,
        Envios.cliente_id == user_id
    )
    envio = db.session.execute(stmt).scalar_one_or_none()
    if not envio:
        return jsonify({"error": "Envío no encontrado"}), 404

    # Actualizamos campos solo si vienen en el body
    envio.pais = data.get("pais", envio.pais)
    envio.provincia = data.get("provincia", envio.provincia)
    envio.ciudad = data.get("ciudad", envio.ciudad)
    envio.direccion = data.get("direccion", envio.direccion)
    envio.codigo_postal = data.get("codigo_postal", envio.codigo_postal)
    envio.telefono_contacto = data.get("telefono_contacto", envio.telefono_contacto)

    db.session.commit()
    return jsonify(envio.serialize()), 200

@clients_bp.route('/envios/<int:envio_id>', methods=['DELETE'])
@jwt_required()
def delete_envio(envio_id):
    user_id = get_jwt_identity()
    stmt = select(Envios).where(Envios.id == envio_id, Envios.cliente_id == user_id)
    envio = db.session.execute(stmt).scalar_one_or_none()
    if not envio:
        return jsonify({"error": "Envío no encontrado"}), 404
    db.session.delete(envio)
    db.session.commit()
    return jsonify({"msg": "Envío eliminado correctamente"}), 200

@clients_bp.route('/productos', methods=['GET'])
def get_productos_public():
    stmt = select(Productos).where(Productos.activo == True)
    productos= db.session.execute(stmt).scalars().all()
    return jsonify([p.serialize() for p in productos]), 200

@clients_bp.route('/productos/<int:producto_id>', methods=['GET'])
def get_one_producto(producto_id):
    stmt = select(Productos).where(Productos.id == producto_id, Productos.activo == True)
    producto = db.session.execute(stmt).scalar_one_or_none()
    if not producto :
        return jsonify({"error": "Producto no disponible"}), 404
    return jsonify(producto.serialize()), 200

@clients_bp.route('/productos/buscar', methods=['GET'])
def buscar_productos():
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify({"error": "Debe proporcionar un término de búsqueda"}), 400
    stmt = select(Productos).where(
        Productos.activo == True,
        (Productos.nombre.ilike(f"%{query}%")) |
        (Productos.descripcion.ilike(f"%{query}%"))
    )
    productos = db.session.execute(stmt).scalars().all()
    return jsonify([p.serialize() for p in productos]), 200

# Variantes de productos (solo lectura)
@clients_bp.route('/productos/<int:producto_id>/variantes', methods=['GET'])
def get_variantes_public(producto_id):
    stmt = select(VariantesProductos).where(
        VariantesProductos.id_producto == producto_id,
        VariantesProductos.activo == True
    )
    variantes = db.session.execute(stmt).scalars().all()
    if not variantes:
        return jsonify({"error": "No hay variantes disponibles para este producto"}), 404
    return jsonify([v.serialize() for v in variantes]), 200

@clients_bp.route('/variantes/<int:variante_id>', methods=['GET'])
def get_variante_public(variante_id):
    stmt = select(VariantesProductos).where(
        VariantesProductos.id == variante_id,
        VariantesProductos.activo == True
    )
    variante = db.session.execute(stmt).scalar_one_or_none()
    if not variante:
        return jsonify({"error": "Variante no disponible"}), 404
    return jsonify(variante.serialize()), 200

#enpoint cliente promociones
@clients_bp.route('/promociones/aplicar', methods=['POST'])
@jwt_required
def aplicar_promocion():
    identity = get_jwt_identity()  # ID del cliente logueado
    data = request.get_json()
    codigo = data.get("codigo")
    items = data.get("items", [])
    if not codigo or not items:
        return jsonify({"error": "Debe enviar el código y la lista de items"}), 400
    # Buscar al cliente (por si luego quieres registrar la promo aplicada en su carrito/checkout)
    cliente = Users.query.get(identity)
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404
    # Buscar la promoción
    promo = Promociones.query.filter_by(codigo_promocional=codigo, activo=True).first()
    if not promo:
        return jsonify({"error": "Código no válido"}), 404
    if not promo.es_valida():
        return jsonify({"error": "La promoción no está vigente"}), 400
    total_original = 0.0
    detalle_items = []
    for item in items:
        variante_id = item.get("variante_id")
        cantidad = item.get("cantidad", 0)
        if not variante_id or cantidad <= 0:
            return jsonify({"error": "Cada item debe tener variante_id y cantidad > 0"}), 400
        # Buscar la variante en BD
        variante = VariantesProductos.query.get(variante_id)
        if not variante or not variante.activo:
            return jsonify({"error": f"Variante {variante_id} no disponible"}), 404
        if cantidad > variante.stock:
            return jsonify({"error": f"No hay suficiente stock para {variante.atributo} {variante.valor}"}), 400
        subtotal = float(variante.precio) * cantidad
        total_original += subtotal
        detalle_items.append({
            "variante_id": variante.id,
            "atributo": variante.atributo,
            "valor": variante.valor,
            "precio_unitario": float(variante.precio),
            "cantidad": cantidad,
            "subtotal": subtotal
        })
    # Calcular descuento
    descuento = float(promo.descuento_porcentaje) * total_original
    total_con_descuento = total_original - descuento
    return jsonify({
        "cliente_id": cliente.id,   # 🔹 Aquí ves qué cliente aplicó la promo
        "codigo_promocional": promo.codigo_promocional,
        "descuento_porcentaje": str(promo.descuento_porcentaje),
        "total_original": round(total_original, 2),
        "total_con_descuento": round(total_con_descuento, 2),
        "items": detalle_items
    }), 200

#Enpoints ventas 
@clients_bp.route('/ventas', methods=['POST'])
@jwt_required()
def create_venta_cliente():
    user_id = get_jwt_identity()
    # Verificar que el cliente exista
    stmt_cliente = select(Clientes).where(Clientes.user_id == user_id)
    cliente = db.session.execute(stmt_cliente).scalar_one_or_none()
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404
    data = request.get_json()
    items = data.get("items", [])
    if not items:
        return jsonify({"error": "Debe incluir al menos un producto en items"}), 400
    if not data.get("id_envio"):
        return jsonify({"error": "id_envio son obligatorios"}), 400
    # Verificar envío
    stmt_envio = select(Envios).where(Envios.id == data["id_envio"])
    envio = db.session.execute(stmt_envio).scalar_one_or_none()
    if not envio:
        return jsonify({"error": "Envío no encontrado"}), 404
    # Calcular subtotal a partir de items
    sub_total = sum(
        Decimal(str(item["precio_unidad"])) * int(item["cantidad"])
        for item in items
    )
    venta = Ventas(
        id_cliente=cliente.user_id,
        id_envio=data["id_envio"],
        sub_total=sub_total,
        numero_seguimiento=data.get("numero_seguimiento")
    )
    # Si el cliente usa un código promocional
    if "id_promo" in data:
        stmt_promo = select(Promociones).where(Promociones.id == data["id_promo"])
        promo = db.session.execute(stmt_promo).scalar_one_or_none()
        if promo:
            venta.aplicar_promocion(promo)
    venta.calcular_totales()
    db.session.add(venta)
    db.session.flush()
    # Crear los detalles de la venta
    detalles_serializados = []
    for item in items:
        # Verificar variante de producto
        stmt_var = select(VariantesProductos).where(VariantesProductos.id == item["id_variante_prod"])
        variante = db.session.execute(stmt_var).scalar_one_or_none()
        if not variante:
            return jsonify({"error": f"Variante de producto {item['id_variante_prod']} no encontrada"}), 404
        detalle = DetallesVentas(
            id_venta=venta.id,
            id_variante_prod=item["id_variante_prod"],
            cantidad=item["cantidad"],
            precio_unidad=Decimal(str(item["precio_unidad"]))
        )
        db.session.add(detalle)
        db.session.flush()
        # Serializar detalle incluyendo info de producto y variante
        detalles_serializados.append({
            "id": detalle.id,
            "id_venta": detalle.id_venta,
            "id_variante_prod": detalle.id_variante_prod,
            "cantidad": detalle.cantidad,
            "precio_unidad": str(detalle.precio_unidad),
            "producto": {
                "nombre": variante.producto.nombre if variante.producto else None,
                "variante": variante.nombre
            }
        })

    db.session.commit()
    return jsonify({
        "venta": venta.serialize(),
        "detalles": detalles_serializados
    }), 201

@clients_bp.route('/ventas/mis-ventas', methods=['GET'])
@jwt_required()
def get_mis_ventas():
    user_id = get_jwt_identity()
    stmt = select(Ventas).where(Ventas.id_cliente == user_id)
    ventas = db.session.execute(stmt).scalars().all()
    return jsonify([v.serialize() for v in ventas]), 200

@clients_bp.route('/ventas/<int:venta_id>', methods=['GET'])
@jwt_required()
def get_mi_venta(venta_id):
    user_id = get_jwt_identity()
    stmt = select(Ventas).where(Ventas.id == venta_id, Ventas.id_cliente == user_id)
    venta = db.session.execute(stmt).scalar_one_or_none()
    if not venta:
        return jsonify({"error": "Venta no encontrada o no pertenece al cliente"}), 404
    return jsonify(venta.serialize()), 200

@clients_bp.route('/ventas/<int:venta_id>/detalles', methods=['GET'])
@jwt_required()
def get_mis_detalles_venta(venta_id):
    user_id = get_jwt_identity()
    stmt = select(Ventas).where(Ventas.id == venta_id, Ventas.id_cliente == user_id)
    venta = db.session.execute(stmt).scalar_one_or_none()
    if not venta:
        return jsonify({"error": "Venta no encontrada o no pertenece al cliente"}), 404
    return jsonify([d.serialize() for d in venta.detalle_venta]), 200

@clients_bp.route('/ventas/<int:venta_id>/detalles/<int:detalle_id>', methods=['GET'])
@jwt_required()
def get_mi_detalle_venta(venta_id, detalle_id):
    user_id = get_jwt_identity()
    stmt = select(DetallesVentas).join(Ventas).where(
        DetallesVentas.id == detalle_id,
        DetallesVentas.id_venta == venta_id,
        Ventas.id_cliente == user_id
    )
    detalle = db.session.execute(stmt).scalar_one_or_none()
    if not detalle:
        return jsonify({"error": "Detalle no encontrado o no pertenece al cliente"}), 404
    return jsonify(detalle.serialize()), 200
#Enpoints reviews
@clients_bp.route('/productos/<int:producto_id>/reviews', methods=['POST'])
@jwt_required()
def create_review_cliente(producto_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    if not data.get("mensaje") or not data.get("rate"):
        return jsonify({"error": "mensaje y rate son obligatorios"}), 400
    # Verificar que el cliente exista
    stmt_cliente = select(Clientes).where(Clientes.user_id == user_id)
    cliente = db.session.execute(stmt_cliente).scalar_one_or_none()
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404
    # Verificar que el producto exista
    stmt_prod = select(Productos).where(Productos.id == producto_id)
    producto = db.session.execute(stmt_prod).scalar_one_or_none()
    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404
    review = Reviews(
        id_cliente=user_id,
        id_producto=producto_id,
        mensaje=data["mensaje"],
        url_imagen=data.get("url_imagen"),
        rate=float(data["rate"])
    )
    db.session.add(review)
    db.session.commit()
    return jsonify(review.serialize()), 201

@clients_bp.route('/reviews/mis-reviews', methods=['GET'])
@jwt_required()
def get_mis_reviews():
    user_id = get_jwt_identity()
    stmt = select(Reviews).where(Reviews.id_cliente == user_id)
    reviews = db.session.execute(stmt).scalars().all()
    return jsonify([r.serialize() for r in reviews]), 200

@clients_bp.route('/reviews/<int:review_id>', methods=['PUT'])
@jwt_required()
def update_mi_review(review_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    review = db.session.get(Reviews, review_id)
    if not review or review.id_cliente != user_id:
        return jsonify({"error": "Review no encontrada"}), 404
    review.mensaje = data.get("mensaje", review.mensaje)
    review.rate = float(data.get("rate", review.rate))
    review.url_imagen = data.get("url_imagen", review.url_imagen)
    db.session.commit()
    return jsonify(review.serialize()), 200

@clients_bp.route('/reviews/<int:review_id>', methods=['DELETE'])
@jwt_required()
def delete_mi_review(review_id):
    user_id = get_jwt_identity()
    stmt_cliente = select(Reviews).where(Reviews.id == review_id)
    review = db.session.execute(stmt_cliente).scalar_one_or_none()
    if not review or review.id_cliente != user_id:
        return jsonify({"error": "Review no encontrada"}), 404
    db.session.delete(review)
    db.session.commit()
    return jsonify({"msg": "Review eliminada correctamente"}), 200

#enpoints favoritos
@clients_bp.route('/favoritos', methods=['POST'])
@jwt_required()
def add_favorito():
    user_id = get_jwt_identity()
    data = request.get_json()
    if not data.get("id_producto"):
        return jsonify({"error": "id_producto es obligatorio"}), 400
    # Verificar cliente
    stmt_cliente = select(Clientes).where(Clientes.user_id == user_id)
    cliente = db.session.execute(stmt_cliente).scalar_one_or_none()
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404
    # Verificar producto
    stmt_prod = select(Productos).where(Productos.id == data["id_producto"])
    producto = db.session.execute(stmt_prod).scalar_one_or_none()
    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404
    # Evitar duplicados
    existing = Favoritos.query.filter_by(id_cliente=user_id, id_producto=data["id_producto"]).first()
    if existing:
        return jsonify({"error": "Producto ya está en favoritos"}), 409
    favorito = Favoritos(
        id_cliente=user_id,
        id_producto=data["id_producto"]
    )
    db.session.add(favorito)
    db.session.commit()
    return jsonify(favorito.serialize()), 201

@clients_bp.route('/favoritos', methods=['GET'])
@jwt_required()
def get_favoritos():
    user_id = get_jwt_identity()
    stmt = select(Favoritos).where(Favoritos.id_cliente == user_id)
    favoritos = db.session.execute(stmt).scalars().all()
    return jsonify([f.serialize() for f in favoritos]), 200

@clients_bp.route('/favoritos/<int:favorito_id>', methods=['DELETE'])
@jwt_required()
def delete_favorito(favorito_id):
    user_id = get_jwt_identity()
    favorito = db.session.get(Favoritos, favorito_id)
    if not favorito or favorito.id_cliente != user_id:
        return jsonify({"error": "Favorito no encontrado"}), 404
    db.session.delete(favorito)
    db.session.commit()
    return jsonify({"msg": "Favorito eliminado correctamente"}), 200

@clients_bp.route('/pagos', methods=['POST'])
@jwt_required()
def create_pago_seguro():
    user_id = get_jwt_identity()
    data = request.get_json()
    required_fields = ["id_venta", "metodo_pago", "token_transaccion", "ultimos_4_digitos"]
    missing = [f for f in required_fields if not data.get(f)]
    if missing:
        return jsonify({"error": f"Faltan campos obligatorios: {', '.join(missing)}"}), 400
    # Verificar que la venta exista y pertenezca al cliente
    venta = db.session.get(Ventas, data["id_venta"])
    if not venta or venta.id_cliente != user_id:
        return jsonify({"error": "Venta no encontrada o no pertenece al cliente"}), 404
    # Verificar si la venta ya fue pagada
    pagos_existentes = sum([p.monto for p in venta.pago])
    if pagos_existentes >= venta.total:
        return jsonify({"error": "Esta venta ya fue pagada"}), 400
    # Validar monto: si no viene, se asume que paga el total restante
    monto_pago = Decimal(str(data.get("monto", venta.total - pagos_existentes)))
    # Verificar que el monto no exceda el total restante
    total_restante = venta.total - pagos_existentes
    if monto_pago > total_restante:
        return jsonify({"error": f"El monto no puede superar el total restante: {total_restante}"}), 400
    # Crear el pago
    pago = Pagos(
        id_venta=venta.id,
        monto=monto_pago,
        metodo_pago=data["metodo_pago"],
        token_transaccion=data["token_transaccion"],
        ultimos_4_digitos=data["ultimos_4_digitos"],
        detalles=data.get("detalles")
    )
    db.session.add(pago)
    db.session.commit()
    return jsonify(pago.serialize()), 201

@clients_bp.route('/pagos', methods=['GET'])
@jwt_required()
def get_mis_pagos():
    user_id = get_jwt_identity()
    stmt = select(Pagos).join(Ventas).where(Ventas.id_cliente == user_id)
    pagos = db.session.execute(stmt).scalars().all()
    return jsonify([p.serialize() for p in pagos]), 200




    
