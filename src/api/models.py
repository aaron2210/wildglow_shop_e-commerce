from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, DateTime, ForeignKey, Float, Integer, event, Numeric
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column, relationship, object_session
from sqlalchemy.orm.attributes import get_history
from werkzeug.security import generate_password_hash, check_password_hash
from enum import Enum as PyEnum
from datetime import datetime, timezone
from sqlalchemy import Enum as SQLAEnum

db = SQLAlchemy()

IVA = Decimal("0.21")
COSTO_ENVIO_BASE = Decimal("4.5")
ENVIO_GRATIS_DESDE = Decimal("50.0")

class enumRol(PyEnum):
    CLIENTE = "CLIENTE"
    ADMIN = "ADMIN"

class enumDocument(PyEnum):
    DNI = "DNI"
    NIE = "NIE"
    PASAPORTE = "PASAPORTE"


class enumGenero(PyEnum):
    MASCULINO = "MASCULINO"
    FEMENINO = "FEMENINO"
    OTROS = "OTROS"
    NINGUNA = "NINGUNA"


class enumMetodoPago(PyEnum):
    TARJETA = "TARJETA"
    PAYPAL = "PAYPAL"


class enumEstadoEnvio(PyEnum):
    PENDIENTE = "PENDIENTE"
    EN_TRANSITO = "EN TRANSITO"
    ENTREGADO = "ENTREGADO"
    CANCELADO = "CANCELADO"


class enumEstadoPago(PyEnum):
    PENDIENTE = "PENDIENTE"
    PROCESANDO = "PROCESANDO"
    APROBADO = "APROBADO"
    RECHAZADO = "RECHAZADO"
    CANCELADO = "CANCELADO"
    REEMBOLSADO = "REEMBOLSADO"
    FALLIDO = "FALLIDO"


class Users(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    rol: Mapped[enumRol] = mapped_column(SQLAEnum(enumRol), default=enumRol.CLIENTE)
    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime(), default=datetime.now(timezone.utc))

    cliente: Mapped["Clientes"] = relationship(
        "Clientes", back_populates="user", uselist=False)
    
    def set_password(self, raw_password: str):
        self.password = generate_password_hash(raw_password)

    def check_password(self, raw_password: str) -> bool:
        return check_password_hash(self.password, raw_password)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "rol": self.rol.value,
            "fecha_creacion": self.fecha_creacion.isoformat()
        }


class Clientes(db.Model):
    __tablename__ = "clientes"
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), primary_key=True)
    tipo_documento: Mapped[enumDocument] = mapped_column(
        SQLAEnum(enumDocument))
    documento_identidad: Mapped[str] = mapped_column(
        String(15), unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String(30), nullable=False)
    apellido_paterno: Mapped[str] = mapped_column(String(20), nullable=False)
    apellido_materno: Mapped[str] = mapped_column(String(20), nullable=False)
    genero: Mapped[enumGenero] = mapped_column(
        SQLAEnum(enumGenero), default=enumGenero.NINGUNA)
    fecha_nacimiento: Mapped[datetime] = mapped_column(
        DateTime(), nullable=True)
    telefono: Mapped[str] = mapped_column(
        String(15), unique=True, nullable=False)
    avatar_url: Mapped[str] = mapped_column(String(
        300), default="https://e7.pngegg.com/pngimages/949/339/png-clipart-avatar-profile-pic-masculine-man-human-character-person.png")

    user: Mapped["Users"] = relationship(back_populates="cliente")
    envio: Mapped[list["Envios"]] = relationship(
        back_populates="cliente", cascade="all, delete-orphan")
    review: Mapped[list["Reviews"]] = relationship(
        back_populates="cliente", cascade="all, delete-orphan")
    favorito: Mapped[list["Favoritos"]] = relationship(
        back_populates="cliente", cascade="all, delete-orphan")
    venta: Mapped[list["Ventas"]] = relationship(
        back_populates="cliente", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.user_id,
            "tipo_documento": self.tipo_documento.value,
            "documento": self.documento_identidad,
            "nombre": self.nombre,
            "apellido_paterno": self.apellido_paterno,
            "apellido_materno": self.apellido_materno,
            "genero": self.genero.value,
            "fecha_nacimiento": self.fecha_nacimiento.isoformat() if self.fecha_nacimiento else None,
            "telefono": self.telefono,
            "avatar_url": self.avatar_url,
            "envio": [e.serialize() for e in self.envio],
            "favorito": [f.serialize() for f in self.favorito],
            "venta": [v.serialize() for v in self.venta],
            "review": [r.serialize() for r in self.review]
        }


class Envios(db.Model):
    __tablename__ = "envios"
    id: Mapped[int] = mapped_column(primary_key=True)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("clientes.user_id"))
    pais: Mapped[str] = mapped_column(String(15), nullable=False)
    provincia: Mapped[str] = mapped_column(String(20), nullable=False)
    ciudad: Mapped[str] = mapped_column(String(20), nullable=False)
    direccion: Mapped[str] = mapped_column(String(150), nullable=False)
    codigo_postal: Mapped[str] = mapped_column(String(10), nullable=False)
    telefono_contacto: Mapped[str] = mapped_column(String(15), nullable=False)

    cliente: Mapped["Clientes"] = relationship(back_populates="envio")
    venta: Mapped["Ventas"] = relationship(back_populates="envio")

    def serialize(self):
        return {
            "id": self.id,
            "cliente_id": self.cliente_id,
            "pais": self.pais,
            "provincia": self.provincia,
            "ciudad": self.ciudad,
            "direccion": self.direccion,
            "codigo_postal": self.codigo_postal,
            "telefono_contacto": self.telefono_contacto
        }


class Categorias(db.Model):
    __tablename__ = "categorias"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(15), nullable=False)
    descripcion: Mapped[str] = mapped_column(String(300), nullable=False)

    producto: Mapped[list["Productos"]] = relationship(
        back_populates="categoria")

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "producto": [prod.serialize() for prod in self.producto]
        }


class Productos(db.Model):
    __tablename__ = "productos"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    id_categoria: Mapped[int] = mapped_column(ForeignKey("categorias.id"))
    descripcion: Mapped[str] = mapped_column(String(300), nullable=False)
    imagen_url: Mapped[str] = mapped_column(String(300), nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

    categoria: Mapped["Categorias"] = relationship(back_populates="producto")
    variante_producto: Mapped[list["VariantesProductos"]
                              ] = relationship(back_populates="producto", cascade="all, delete-orphan")
    review: Mapped[list["Reviews"]] = relationship(
        back_populates="producto", cascade="all, delete-orphan")
    favorito: Mapped[list["Favoritos"]] = relationship(
        back_populates="producto", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "id_categoria": self.id_categoria,
            "descripcion": self.descripcion,
            "imagen_url": self.imagen_url,
            "activo": self.activo,
            "variante_producto": [v.serialize() for v in self.variante_producto]
        }


class Promociones(db.Model):
    __tablename__ = "promociones"
    id: Mapped[int] = mapped_column(primary_key=True)
    codigo_promocional: Mapped[str] = mapped_column(
        String(20), unique=True, nullable=False)
    descuento_porcentaje: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), default=0.10, nullable=False)
    fecha_inicio: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    fecha_fin: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

    venta: Mapped["Ventas"] = relationship(back_populates="promo")

    def es_valida(self) -> bool:
        ahora = datetime.now(timezone.utc)
        return (
            self.activo
            and self.fecha_inicio <= ahora <= self.fecha_fin
            # asegura que no haya sido usada en ninguna venta
            and len(self.venta) == 0
        )

    def serialize(self):
        return {
            "id": self.id,
            "codigo_promocional": self.codigo_promocional,
            "descuento_porcentaje": str(self.descuento_porcentaje),
            "fecha_inicio": self.fecha_inicio.isoformat(),
            "fecha_fin": self.fecha_fin.isoformat(),
            "activo": self.activo
        }


class VariantesProductos(db.Model):
    __tablename__ = "varianteProducto"
    id: Mapped[int] = mapped_column(primary_key=True)
    id_producto: Mapped[int] = mapped_column(ForeignKey("productos.id"))
    atributo: Mapped[str] = mapped_column(String(50), nullable=False)
    valor: Mapped[str] = mapped_column(String(50), nullable=False)
    precio: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    stock: Mapped[int] = mapped_column(default=0, nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    producto: Mapped["Productos"] = relationship(
        back_populates="variante_producto")
    detalle_venta: Mapped[list["DetallesVentas"]] = relationship(
        back_populates="variante_prod")

    def ajustar_stock(self, cantidad):
        if cantidad > 0 and cantidad > self.stock:
            raise ValueError(
            f"No hay suficiente stock para {self.atributo} {self.valor}. "
            f"Stock actual: {self.stock}, solicitado: {cantidad}"
        )
        self.stock -= cantidad

    def serialize(self):
                return {
                    "id": self.id,
                    "id_producto": self.id_producto,
                    "atributo": self.atributo,
                    "valor": self.valor,
                    "precio": str(self.precio),
                    "stock": self.stock,
                    "activo": self.activo
                }


class Reviews(db.Model):
    __tablename__ = "reviews"
    id: Mapped[int] = mapped_column(primary_key=True)
    id_cliente: Mapped[int] = mapped_column(ForeignKey("clientes.user_id"))
    id_producto: Mapped[int] = mapped_column(ForeignKey("productos.id"))
    mensaje: Mapped[str] = mapped_column(String(300), nullable=False)
    url_imagen: Mapped[str] = mapped_column(String(300), nullable=True)
    rate: Mapped[float] = mapped_column(default=0.0, nullable=False)

    cliente: Mapped["Clientes"] = relationship(back_populates="review")
    producto: Mapped["Productos"] = relationship(back_populates="review")

    def serialize(self):
        return {
            "id": self.id,
            "id_cliente": self.id_cliente,
            "id_producto": self.id_producto,
            "mensaje": self.mensaje,
            "url_imagen": self.url_imagen,
            "rate": self.rate
        }


@event.listens_for(Reviews, "before_insert")
@event.listens_for(Reviews, "before_update")
def validar_rate(mapper, connection, target):
    if target.rate < 1 or target.rate > 5:
        raise ValueError("La valoración debe estar entre 1 y 5 estrellas.")


class Favoritos(db.Model):
    __tablename__ = "favoritos"
    id: Mapped[int] = mapped_column(primary_key=True)
    id_producto: Mapped[int] = mapped_column(ForeignKey("productos.id"))
    id_cliente: Mapped[int] = mapped_column(ForeignKey("clientes.user_id"))

    producto: Mapped["Productos"] = relationship(back_populates="favorito")
    cliente: Mapped["Clientes"] = relationship(back_populates="favorito")

    def serialize(self):
        return {
            "id": self.id,
            "id_cliente": self.id_cliente,
            "producto": self.producto.serialize()
        }


class Ventas(db.Model):
    __tablename__ = "ventas"
    id: Mapped[int] = mapped_column(primary_key=True)
    id_cliente: Mapped[int] = mapped_column(ForeignKey("clientes.user_id"))
    id_envio: Mapped[int] = mapped_column(ForeignKey("envios.id"))
    id_promo: Mapped[int | None] = mapped_column(
        ForeignKey("promociones.id"), nullable=True)
    fecha_venta: Mapped[datetime] = mapped_column(
        DateTime(), default=datetime.now(timezone.utc))
    sub_total: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), default=0.0, nullable=False)
    descuento_total: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), default=0.0, nullable=False)
    iva_aplicado: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), default=0.0, nullable=False)
    costo_envio_final: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), default=0.0, nullable=False)
    total: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    estado_envio: Mapped[enumEstadoEnvio] = mapped_column(
        SQLAEnum(enumEstadoEnvio), default=enumEstadoEnvio.PENDIENTE)
    numero_seguimiento: Mapped[str] = mapped_column(String(30), nullable=True)

    cliente: Mapped["Clientes"] = relationship(back_populates="venta")
    envio: Mapped["Envios"] = relationship(back_populates="venta")
    promo: Mapped["Promociones"] = relationship(back_populates="venta")
    detalle_venta: Mapped[list["DetallesVentas"]
                          ] = relationship(back_populates="venta", cascade="all, delete-orphan")
    pago: Mapped[list["Pagos"]] = relationship(
        back_populates="venta", cascade="all, delete-orphan")

    def aplicar_promocion(self, promo: "Promociones"):
        if promo and promo.es_valida():
            self.descuento_total = (
                self.sub_total * promo.descuento_porcentaje).quantize(Decimal("0.01"))
            self.id_promo = promo.id
        else:
            self.descuento_total = Decimal("0.00")
        self.calcular_totales()

    def calcular_totales(self):
        self.iva_aplicado = self.sub_total*IVA
        self.costo_envio_final = 0 if self.sub_total >= ENVIO_GRATIS_DESDE else COSTO_ENVIO_BASE
        self.total = (self.sub_total + self.iva_aplicado +
                      self.costo_envio_final) - self.descuento_total

    def serialize(self):
        return {
            "id": self.id,
            "id_cliente": self.id_cliente,
            "id_envio": self.id_envio,
            "id_promo": self.id_promo,
            "fecha_venta": self.fecha_venta.isoformat(),
            "sub_total": str(self.sub_total),
            "iva_aplicado": str(self.iva_aplicado),
            "descuento_total": str(self.descuento_total),
            "costo_envio_final": str(self.costo_envio_final),
            "total": str(self.total),
            "estado_envio": self.estado_envio.value,
            "numero_seguimiento": self.numero_seguimiento
        }


@event.listens_for(Ventas, "before_insert")
def before_insert(mapper, connection, target):
    target.calcular_totales()


@event.listens_for(Ventas, "before_update")
def before_update(mapper, connection, target):
    target.calcular_totales()


class DetallesVentas(db.Model):
    __tablename__ = "detallesVentas"
    id: Mapped[int] = mapped_column(primary_key=True)
    id_venta: Mapped[int] = mapped_column(ForeignKey("ventas.id"))
    id_variante_prod: Mapped[int] = mapped_column(
        ForeignKey("varianteProducto.id"))
    cantidad: Mapped[int] = mapped_column(default=0, nullable=False)
    precio_unidad: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False)

    venta: Mapped["Ventas"] = relationship(back_populates="detalle_venta")
    variante_prod: Mapped["VariantesProductos"] = relationship(
        back_populates="detalle_venta")

    def serialize(self):
        return {
            "id": self.id,
            "id_venta": self.id_venta,
            "id_variante_prod": self.id_variante_prod,
            "cantidad": self.cantidad,
            "precio_unidad": str(self.precio_unidad),
            "producto":{
                "nombre": self.variante_prod.producto.nombre if self.variante_prod and self.variante_prod.producto else None,
                "atributo": self.variante_prod.atributo if self.variante_prod else None,
                "valor": self.variante_prod.valor if self.variante_prod else None
            }
        }


@event.listens_for(DetallesVentas, "before_insert")
def restar_stock_antes_insert(mapper, connection, target):
    session = object_session(target)
    variante = session.query(VariantesProductos).with_for_update().get(
        target.id_variante_prod)
    if not variante:
        raise ValueError("La variante de producto no existe.")

    variante.ajustar_stock(target.cantidad)


@event.listens_for(DetallesVentas, "before_update")
def actualizar_stock_antes_update(mapper, connection, target):
    session = object_session(target)
    variante = session.query(VariantesProductos).with_for_update().get(
        target.id_variante_prod)
    if not variante:
        raise ValueError("La variante de producto no existe.")

    # Obtener diferencia entre cantidad nueva y antigua
    hist = get_history(target, 'cantidad')
    vieja_cantidad = hist.deleted[0] if hist.deleted else 0
    nueva_cantidad = target.cantidad
    diferencia = nueva_cantidad - vieja_cantidad

    variante.ajustar_stock(diferencia)


@event.listens_for(DetallesVentas, "before_delete")
def devolver_stock_antes_delete(mapper, connection, target):
    session = object_session(target)
    variante = session.query(VariantesProductos).with_for_update().get(
        target.id_variante_prod)
    if variante:
        # cantidad negativa = devolver stock
        variante.ajustar_stock(-target.cantidad)


class Pagos(db.Model):
    __tablename__ = "pagos"
    id: Mapped[int] = mapped_column(primary_key=True)
    id_venta: Mapped[int] = mapped_column(ForeignKey("ventas.id"))
    fecha_pago: Mapped[datetime] = mapped_column(
        DateTime(), default=datetime.now(timezone.utc))
    monto: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    metodo_pago: Mapped[enumMetodoPago] = mapped_column(
        SQLAEnum(enumMetodoPago), default=enumMetodoPago.TARJETA)
    token_transaccion: Mapped[str] = mapped_column(String(300), nullable=False)
    ultimos_4_digitos: Mapped[str] = mapped_column(String(4), nullable=False)
    estado: Mapped[enumEstadoPago] = mapped_column(
        SQLAEnum(enumEstadoPago), default=enumEstadoPago.PENDIENTE)
    detalles: Mapped[str] = mapped_column(String(300))

    venta: Mapped["Ventas"] = relationship(back_populates="pago")

    def serialize(self):
        return {
            "id": self.id,
            "id_venta": self.id_venta,
            "fecha_pago": self.fecha_pago.isoformat(),
            "monto": str(self.monto),
            "metodo_pago": self.metodo_pago.value,
            "token_transaccion": self.token_transaccion,
            "ultimos_4_digitos": self.ultimos_4_digitos,
            "estado": self.estado.value,
            "detalles": self.detalles
        }
