from flask import Blueprint, render_template, request, redirect, url_for, session
from app.models.novel import Novel, Chapter
from app.models.record import Record, Collection

reader_bp = Blueprint('reader', __name__)

@reader_bp.route('/novel/<int:novel_id>')
def detail(novel_id):
    """
    小說詳情頁。
    顯示小說簡介、作者資訊與所有章節列表。
    """
    pass

@reader_bp.route('/novel/<int:novel_id>/read/<int:chapter_num>')
def read(novel_id, chapter_num):
    """
    閱讀介面。
    顯示特定章節內容，並自動紀錄/更新讀者的閱讀進度。
    """
    pass

@reader_bp.route('/novel/<int:novel_id>/collect', methods=['POST'])
def collect(novel_id):
    """
    收藏操作。
    切換（新增/刪除）該小說在使用者書單中的狀態。
    """
    pass

@reader_bp.route('/profile')
def profile():
    """
    個人中心 (我的書架)。
    顯示使用者的閱讀紀錄與收藏書單。
    需要登入驗證。
    """
    pass
