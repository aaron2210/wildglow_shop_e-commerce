  
import os
from flask_admin import Admin
from src.api.models import db, Users, Clientes, Envios, Categorias, Productos, Promociones, VariantesProductos, Reviews, Favoritos, Ventas, DetallesVentas, Pagos
from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(ModelView(Users, db.session))
    admin.add_view(ModelView(Clientes, db.session))
    admin.add_view(ModelView(Envios, db.session))
    admin.add_view(ModelView(Categorias, db.session))
    admin.add_view(ModelView(Productos, db.session))
    admin.add_view(ModelView(Promociones, db.session))
    admin.add_view(ModelView(VariantesProductos, db.session))
    admin.add_view(ModelView(Reviews, db.session))
    admin.add_view(ModelView(Favoritos, db.session))
    admin.add_view(ModelView(Ventas, db.session))
    admin.add_view(ModelView(DetallesVentas, db.session))
    admin.add_view(ModelView(Pagos, db.session))

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))