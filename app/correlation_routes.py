from flask import Blueprint,jsonify
from app.services.correlation_service import get_correlation_metrics

correlation_bp = Blueprint('correlation',__name__)
#create route for correlation_bp
@correlation_bp.route('/<ticker>',methods=['GET'])
def get_correlation_data(ticker):
    data=get_correlation_metrics(ticker)
    return jsonify(data)