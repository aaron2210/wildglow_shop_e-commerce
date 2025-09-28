from app import app
from api.models import db, Users, Clientes, Envios, Reviews, Favoritos, Ventas, Promociones, Pagos, DetallesVentas, Productos, Categorias, VariantesProductos
from api.models import enumDocument, enumEstadoEnvio, enumEstadoPago, enumGenero, enumMetodoPago, enumRol
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from werkzeug.security import generate_password_hash, check_password_hash

with app.app_context():
    db.drop_all()
    db.create_all()
    #Usuarios
    users=[
        Users(email="juan@example.com", password=generate_password_hash("password123"), rol=enumRol.CLIENTE),
        Users(email="maria@example.com", password=generate_password_hash("password123"), rol=enumRol.CLIENTE),
        Users(email="luis@example.com", password=generate_password_hash("password123"), rol=enumRol.CLIENTE),
        Users(email="ana@example.com", password=generate_password_hash("password123"), rol=enumRol.CLIENTE),
        Users(email="carlos@example.com", password=generate_password_hash("password123"), rol=enumRol.CLIENTE),
    ]
    db.session.add_all(users)
    db.session.flush()  # para obtener IDs
    db.session.commit()

    clientes = [
        Clientes(user_id=users[0].id, tipo_documento=enumDocument.DNI, documento_identidad="12345678", nombre="Juan", apellido_paterno="Pérez", apellido_materno="García", genero=enumGenero.MASCULINO, fecha_nacimiento=datetime(1990,5,20), telefono="600111222"),
        Clientes(user_id=users[1].id, tipo_documento=enumDocument.DNI, documento_identidad="87654321", nombre="María", apellido_paterno="López", apellido_materno="Martínez", genero=enumGenero.FEMENINO, fecha_nacimiento=datetime(1995,8,15), telefono="600333444"),
        Clientes(user_id=users[2].id, tipo_documento=enumDocument.DNI, documento_identidad="11223344", nombre="Luis", apellido_paterno="Ramírez", apellido_materno="Torres", genero=enumGenero.MASCULINO, fecha_nacimiento=datetime(1988,2,10), telefono="600777888"),
        Clientes(user_id=users[3].id, tipo_documento=enumDocument.DNI, documento_identidad="44332211", nombre="Ana", apellido_paterno="Fernández", apellido_materno="Gómez", genero=enumGenero.FEMENINO, fecha_nacimiento=datetime(1992,11,25), telefono="600999000"),
        Clientes(user_id=users[4].id, tipo_documento=enumDocument.NIE, documento_identidad="X9876543Z", nombre="Carlos", apellido_paterno="Mendoza", apellido_materno="Ruiz", genero=enumGenero.MASCULINO, fecha_nacimiento=datetime(1993,7,10), telefono="600112233"),
    ]
    db.session.add_all(clientes)
    db.session.commit()

    envios = [
        Envios(cliente_id=clientes[0].user_id, pais="España", provincia="Valencia", ciudad="Valencia", direccion="Calle Falsa 123", codigo_postal="46001", telefono_contacto="600111222"),
        Envios(cliente_id=clientes[1].user_id, pais="España", provincia="Madrid", ciudad="Madrid", direccion="Gran Vía 45", codigo_postal="28013", telefono_contacto="600333444"),
        Envios(cliente_id=clientes[2].user_id, pais="España", provincia="Sevilla", ciudad="Sevilla", direccion="Av. Constitución 12", codigo_postal="41001", telefono_contacto="600777888"),
        Envios(cliente_id=clientes[3].user_id, pais="España", provincia="Bilbao", ciudad="Bilbao", direccion="Plaza Nueva 7", codigo_postal="48005", telefono_contacto="600999000"),
        Envios(cliente_id=clientes[4].user_id, pais="España", provincia="Barcelona", ciudad="Barcelona", direccion="Diagonal 89", codigo_postal="08029", telefono_contacto="600112233"),
    ]
    db.session.add_all(envios)
    db.session.commit()

    categorias = [
        Categorias(nombre="Velas", descripcion="Velas aromáticas y decorativas."),
        Categorias(nombre="Wax Melts", descripcion="Pastillas aromáticas para quemadores."),
        Categorias(nombre="Quemadores", descripcion="Quemadores de cerámica y eléctricos."),
        Categorias(nombre="Accesorios", descripcion="Mecheros, cortapabilos y más."),
        Categorias(nombre="Packs", descripcion="Sets de regalo y combinaciones."),
    ]
    db.session.add_all(categorias)
    db.session.flush()
    db.session.commit()

    productos = [
        Productos(nombre="Vela Lavanda", id_categoria=categorias[0].id, descripcion="Vela relajante con aroma a lavanda.", imagen_url="https://example.com/vela_lavanda.jpg"),
        Productos(nombre="Wax Melt Vainilla", id_categoria=categorias[1].id, descripcion="Pastillas de cera con aroma a vainilla.", imagen_url="https://example.com/wax_vainilla.jpg"),
        Productos(nombre="Quemador Cerámica Blanco", id_categoria=categorias[2].id, descripcion="Quemador elegante de cerámica blanco.", imagen_url="https://example.com/quemador_blanco.jpg"),
        Productos(nombre="Cortapabilo", id_categoria=categorias[3].id, descripcion="Corta la mecha de las velas para mayor duración.", imagen_url="https://example.com/cortapabilo.jpg"),
        Productos(nombre="Pack Relajación", id_categoria=categorias[4].id, descripcion="Set con vela, wax melt y quemador.", imagen_url="https://example.com/pack_relajacion.jpg"),
    ]
    db.session.add_all(productos)
    db.session.flush()
    db.session.commit()

    variantes = [
        VariantesProductos(id_producto=productos[0].id, atributo="Tamaño", valor="Pequeña", precio=Decimal("7.99"), stock=50),
        VariantesProductos(id_producto=productos[0].id, atributo="Tamaño", valor="Grande", precio=Decimal("12.99"), stock=30),
        VariantesProductos(id_producto=productos[1].id, atributo="Cantidad", valor="6 unidades", precio=Decimal("4.50"), stock=100),
        VariantesProductos(id_producto=productos[2].id, atributo="Color", valor="Blanco", precio=Decimal("14.99"), stock=20),
        VariantesProductos(id_producto=productos[4].id, atributo="Edición", valor="Premium", precio=Decimal("29.99"), stock=15),
    ]
    db.session.add_all(variantes)
    db.session.commit()

    promociones = [
        Promociones(codigo_promocional="DESC10", descuento_porcentaje=Decimal("0.10"), fecha_inicio=datetime.now(timezone.utc), fecha_fin=datetime.now(timezone.utc)+timedelta(days=30)),
        Promociones(codigo_promocional="VERANO15", descuento_porcentaje=Decimal("0.15"), fecha_inicio=datetime.now(timezone.utc), fecha_fin=datetime.now(timezone.utc)+timedelta(days=60)),
        Promociones(codigo_promocional="NAVIDAD20", descuento_porcentaje=Decimal("0.20"), fecha_inicio=datetime.now(timezone.utc), fecha_fin=datetime.now(timezone.utc)+timedelta(days=90)),
        Promociones(codigo_promocional="WELCOME5", descuento_porcentaje=Decimal("0.05"), fecha_inicio=datetime.now(timezone.utc), fecha_fin=datetime.now(timezone.utc)+timedelta(days=10)),
        Promociones(codigo_promocional="PACK25", descuento_porcentaje=Decimal("0.25"), fecha_inicio=datetime.now(timezone.utc), fecha_fin=datetime.now(timezone.utc)+timedelta(days=45)),
    ]
    db.session.add_all(promociones)
    db.session.commit()

    reviews = [
        Reviews(id_cliente=clientes[0].user_id, id_producto=productos[0].id, mensaje="Excelente vela, huele increíble.", rate=5),
        Reviews(id_cliente=clientes[1].user_id, id_producto=productos[1].id, mensaje="Muy buen aroma, aunque dura poco.", rate=4),
        Reviews(id_cliente=clientes[2].user_id, id_producto=productos[2].id, mensaje="El quemador es elegante y funcional.", rate=5),
        Reviews(id_cliente=clientes[3].user_id, id_producto=productos[3].id, mensaje="Herramienta útil, buen precio.", rate=4),
        Reviews(id_cliente=clientes[4].user_id, id_producto=productos[4].id, mensaje="Pack completo y bonito para regalar.", rate=5),
    ]
    db.session.add_all(reviews)
    db.session.commit()

    favoritos = [
        Favoritos(id_cliente=clientes[0].user_id, id_producto=productos[0].id),
        Favoritos(id_cliente=clientes[1].user_id, id_producto=productos[1].id),
        Favoritos(id_cliente=clientes[2].user_id, id_producto=productos[2].id),
        Favoritos(id_cliente=clientes[3].user_id, id_producto=productos[3].id),
        Favoritos(id_cliente=clientes[4].user_id, id_producto=productos[4].id),
    ]
    db.session.add_all(favoritos)
    db.session.commit()

    ventas = [
        Ventas(
        id_cliente=clientes[0].user_id,
        id_envio=envios[0].id,
        id_promo=promociones[0].id,  # 10% descuento
        sub_total=Decimal("19.98"),
        descuento_total=Decimal("1.99"),
        iva_aplicado=Decimal("4.20"),
        costo_envio_final=Decimal("5.00"),
        total=Decimal("27.19"),
        estado_envio=enumEstadoEnvio.PENDIENTE,
        fecha_venta=datetime.now(),
        numero_seguimiento="PKG123456"
    ),
    Ventas(
        id_cliente=clientes[1].user_id,
        id_envio=envios[1].id,
        id_promo=None,
        sub_total=Decimal("14.99"),
        descuento_total=Decimal("0.00"),
        iva_aplicado=Decimal("3.15"),
        costo_envio_final=Decimal("5.00"),
        total=Decimal("23.14"),
        estado_envio=enumEstadoEnvio.EN_TRANSITO,
        fecha_venta=datetime.now(),
        numero_seguimiento="PKG123457"
    ),
    Ventas(
        id_cliente=clientes[2].user_id,
        id_envio=envios[2].id,
        id_promo=promociones[1].id,  # 15% descuento
        sub_total=Decimal("29.99"),
        descuento_total=Decimal("4.50"),
        iva_aplicado=Decimal("6.30"),
        costo_envio_final=Decimal("0.00"),  # supera el mínimo de envío gratis
        total=Decimal("31.79"),
        estado_envio=enumEstadoEnvio.ENTREGADO,
        fecha_venta=datetime.now(),
        numero_seguimiento="PKG123458"
    ),
    Ventas(
        id_cliente=clientes[3].user_id,
        id_envio=envios[3].id,
        id_promo=None,
        sub_total=Decimal("5.99"),
        descuento_total=Decimal("0.00"),
        iva_aplicado=Decimal("1.26"),
        costo_envio_final=Decimal("5.00"),
        total=Decimal("12.25"),
        estado_envio=enumEstadoEnvio.PENDIENTE,
        fecha_venta=datetime.now(),
        numero_seguimiento="PKG123459"
    ),
    Ventas(
        id_cliente=clientes[4].user_id,
        id_envio=envios[4].id,
        id_promo=promociones[2].id,  # 20% descuento
        sub_total=Decimal("25.98"),
        descuento_total=Decimal("5.20"),
        iva_aplicado=Decimal("5.46"),
        costo_envio_final=Decimal("0.00"),  # supera el mínimo de envío gratis
        total=Decimal("26.24"),
        estado_envio=enumEstadoEnvio.EN_TRANSITO,
        fecha_venta=datetime.now(),
        numero_seguimiento="PKG123460"
    ),
    ]
    db.session.add_all(ventas)
    db.session.flush()
    db.session.commit()

    detalles = [
        DetallesVentas(id_venta=ventas[0].id, id_variante_prod=variantes[0].id, cantidad=2, precio_unidad=Decimal("7.99")),
        DetallesVentas(id_venta=ventas[1].id, id_variante_prod=variantes[3].id, cantidad=1, precio_unidad=Decimal("14.99")),
        DetallesVentas(id_venta=ventas[2].id, id_variante_prod=variantes[4].id, cantidad=1, precio_unidad=Decimal("29.99")),
        DetallesVentas(id_venta=ventas[3].id, id_variante_prod=variantes[2].id, cantidad=1, precio_unidad=Decimal("4.50")),
        DetallesVentas(id_venta=ventas[4].id, id_variante_prod=variantes[1].id, cantidad=2, precio_unidad=Decimal("12.99")),
    ]
    db.session.add_all(detalles)
    db.session.commit()

    pagos = [
        Pagos(id_venta=ventas[0].id, monto=Decimal("19.98"), metodo_pago=enumMetodoPago.TARJETA, token_transaccion="tok_123", ultimos_4_digitos="4242", estado=enumEstadoPago.APROBADO, detalles="Pago exitoso"),
        Pagos(id_venta=ventas[1].id, monto=Decimal("14.99"), metodo_pago=enumMetodoPago.PAYPAL, token_transaccion="tok_456", ultimos_4_digitos="1111", estado=enumEstadoPago.APROBADO, detalles="Pago exitoso"),
        Pagos(id_venta=ventas[2].id, monto=Decimal("24.99"), metodo_pago=enumMetodoPago.TARJETA, token_transaccion="tok_789", ultimos_4_digitos="5555", estado=enumEstadoPago.PENDIENTE, detalles="Pago en proceso"),
        Pagos(id_venta=ventas[3].id, monto=Decimal("5.99"), metodo_pago=enumMetodoPago.TARJETA, token_transaccion="tok_321", ultimos_4_digitos="0000", estado=enumEstadoPago.APROBADO, detalles="Pago completado"),
        Pagos(id_venta=ventas[4].id, monto=Decimal("29.99"), metodo_pago=enumMetodoPago.TARJETA, token_transaccion="tok_654", ultimos_4_digitos="9999", estado=enumEstadoPago.APROBADO, detalles="Pago exitoso"),
    ]
    db.session.add_all(pagos)
    db.session.commit()

print("✅ Datos de seed insertados correctamente.")