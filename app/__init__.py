from flask import Flask
from flask_cors import CORS
from .routes import main_bp
from .reddit_routes import reddit_bp
from .stock_routes import stock_bp
from .correlation_routes import correlation_bp
def create_app():
    app=Flask(__name__)
    CORS(app, resources={r"/*": {"origins": ["http://localhost:5173", "https://sentimentapi.jeremygranizo.tech"]}})
    app.register_blueprint(main_bp) #route is registered
    app.register_blueprint(reddit_bp,url_prefix='/api/reddit')
    app.register_blueprint(stock_bp,url_prefix='/api/stock')
    app.register_blueprint(correlation_bp,url_prefix='/api/correlation')
    #Routes will be registered here
    return app