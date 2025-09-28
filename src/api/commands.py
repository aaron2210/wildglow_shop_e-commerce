
import click
from src.api.models import db, Users, enumRol

"""
In this file, you can add as many commands as you want using the @app.cli.command decorator
Flask commands are usefull to run cronjobs or tasks outside of the API but sill in integration 
with youy database, for example: Import the price of bitcoin every night as 12am
"""
def setup_commands(app):
    
    """ 
    This is an example command "insert-test-users" that you can run from the command line
    by typing: $ flask insert-test-users 5
    Note: 5 is the number of users to add
    """
    @app.cli.command("insert-test-users") # name of our command
    @click.argument("count") # argument of out command
    def insert_test_users(count):
        print("Creating test users")
        for x in range(1, int(count) + 1):
            user = Users()
            user.email = "test_user" + str(x) + "@test.com"
            user.password = "123456"
            user.is_active = True
            db.session.add(user)
            db.session.commit()
            print("User: ", user.email, " created.")

        print("All test users created")

    @app.cli.command("insert-test-data")
    def insert_test_data():
        pass

    @app.cli.command("create-admin")
    def create_admin():
        
        admin_email = "wildandglow.shop@gmail.com"
        admin_pass = "elirolglow951"

        existing = Users.query.filter_by(email=admin_email).first()
        if not existing:
            admin = Users(email=admin_email, rol=enumRol.ADMIN)
            admin.set_password(admin_pass)  # usa hash
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin creado:", admin_email)
        else:
            print("⚠️ El admin ya existe:", admin_email)