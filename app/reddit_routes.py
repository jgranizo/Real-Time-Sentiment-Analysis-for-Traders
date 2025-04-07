from flask import Blueprint, jsonify
from app.services.reddit_service import fetch_reddit_post, get_reddit_data

reddit_bp = Blueprint('reddit', __name__)

@reddit_bp.route('/reddit_fetch', methods=['GET'])
def fetching_reddit_data():
    data=fetch_reddit_post()
    return jsonify(data)

@reddit_bp.route('/<ticker>',methods=['GET'])
def get_reddit_data_by_ticker(ticker):
    data = get_reddit_data(ticker)
    return jsonify(data)
