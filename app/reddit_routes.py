from flask import Blueprint, jsonify
from app.services.reddit_service import get_reddit_metrics
reddit_bp = Blueprint('reddit', __name__)

@reddit_bp.route('/<ticker>', methods=['GET'])
def get_reddit_data(ticker):
    data=get_reddit_metrics(ticker)
    return jsonify(data)
