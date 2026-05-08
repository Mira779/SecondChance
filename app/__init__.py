from flask import Flask 
from app.routes.extensions import db
from flask_migrate import Migrate
from app.routes.raw_routes import raw_bp
from app.routes.main_routes import main_bp
from app.routes.voucher_routes import voucher_bp
from app.metadata.p_route import product_bp


migrate = Migrate()

def create_app():

    app = Flask(__name__)
    migrate.init_app(app, db)

    # Initialize Database 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:$bkmira4564M$@localhost:3306/databasedb'
    app.config['SQLACHEMY_TRACK_MODIFICATIONS'] = False

    app.register_blueprint(main_bp)
    app.register_blueprint(raw_bp)
    app.register_blueprint(voucher_bp)
    app.register_blueprint(product_bp)

    db.init_app(app)

    return app