from flask import Blueprint,jsonify
from app.services.stock_service import get_stock_metrics
#create blueprint for stock first
stock_bp = Blueprint("stock",__name__,)
#create route for stock
@stock_bp.route('/<ticker>',methods=['GET'])
#create function for stock to retrieve dat
def  get_stock_data(ticker):
    data = get_stock_metrics(ticker)
    return jsonify(data)
