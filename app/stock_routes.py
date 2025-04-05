from flask import Blueprint,jsonify,request
from app.services.stock_service import get_stock_data,get_stock_by_date

#create blueprint for stock first
stock_bp = Blueprint("stock",__name__,)
#create route for stock
@stock_bp.route('/<ticker>',methods=['GET'])
#create function for stock to retrieve data
def  fetch_stock_data(ticker):
    
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    if start_date and end_date:
        data = get_stock_by_date(ticker,start_date,end_date)
        if data:
            return jsonify(data),200
        return jsonify({"message": " No data found for the specific date range"}), 404
   
    data = get_stock_data(ticker)
    if data:
        return jsonify(data), 200
    return jsonify({"message": "No data found for the specific ticker"}), 404