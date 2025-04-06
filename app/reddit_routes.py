from flask import Blueprint, jsonify
from app.services.reddit_service import fetch_reddit_post

reddit_bp = Blueprint('reddit', __name__)

@reddit_bp.route('/reddit_fetch', methods=['GET'])
def get_reddit_data():
    data=fetch_reddit_post()
    return jsonify(data)
