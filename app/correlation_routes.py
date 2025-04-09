from flask import Blueprint,jsonify,request
from app.services.correlation_service import get_correlation_metrics
import pandas as pd
correlation_bp = Blueprint('correlation',__name__)
#create route for correlation_bp
@correlation_bp.route('/<ticker>',methods=['GET'])
def get_correlation_data(ticker):

    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    if start_date and end_date:
        data=get_correlation_metrics(ticker,start_date,end_date)
        if data: 
            return data,200
    return jsonify({"message": "No data found for the specified date range"})
    
