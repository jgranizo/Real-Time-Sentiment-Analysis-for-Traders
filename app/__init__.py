from flask import Flask
from flask_cors import CORS
from .routes import main_bp
from .reddit_routes import reddit_bp
from .stock_routes import stock_bp
from .correlation_routes import correlation_bp
import os
from dotenv import load_dotenv
from .extensions import db


load_dotenv()


def create_app():
    app = Flask(__name__)
   
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    CORS(
        app,
        resources={
            r"/*": {
                "origins": [
                    "http://localhost:5173",
                    "https://sentimentapi.jeremygranizo.tech",
                ]
            }
        },
        origins=["http://localhost:5173"]
    )
    
    app.register_blueprint(main_bp)  # route is registered
    app.register_blueprint(reddit_bp, url_prefix="/api/reddit")
    app.register_blueprint(stock_bp, url_prefix="/api/stock")
    app.register_blueprint(correlation_bp, url_prefix="/api/correlation")

    #Initialize database within app context
    with app.app_context():
        db.create_all()
        
    return app
