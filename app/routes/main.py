from flask import Blueprint, render_template, request
from app.models.novel import Novel

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    首頁。
    顯示熱門推薦與最新小說。
    """
    pass

@main_bp.route('/search')
def search():
    """
    搜尋頁面。
    根據關鍵字 `q` 顯示小說搜尋結果。
    """
    pass

@main_bp.route('/ranking')
def ranking():
    """
    排行榜頁面。
    顯示不同類別的小說排行榜。
    """
    pass
