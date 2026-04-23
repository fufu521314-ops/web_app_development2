from flask import Blueprint, render_template, request
from app.models.novel import Novel

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    首頁。
    顯示熱門推薦與最新小說。
    """
    try:
        # 取得熱門小說 (依點擊數 views 排序)
        popular_novels = Novel.query.order_by(Novel.views.desc()).limit(10).all()
        # 取得最新小說
        latest_novels = Novel.query.order_by(Novel.created_at.desc()).limit(10).all()
        return render_template('index.html', popular_novels=popular_novels, latest_novels=latest_novels)
    except Exception as e:
        print(f"首頁載入失敗: {e}")
        return render_template('index.html', popular_novels=[], latest_novels=[])

@main_bp.route('/search')
def search():
    """
    搜尋頁面。
    根據關鍵字 `q` 顯示小說搜尋結果。
    """
    query = request.args.get('q', '')
    if not query:
        return redirect(url_for('main.index'))
    
    try:
        # 模糊搜尋書名或作者
        results = Novel.query.filter(
            (Novel.title.like(f"%{query}%")) | (Novel.author.like(f"%{query}%"))
        ).all()
        return render_template('search.html', results=results, query=query)
    except Exception as e:
        print(f"搜尋失敗: {e}")
        return render_template('search.html', results=[], query=query)

@main_bp.route('/ranking')
def ranking():
    """
    排行榜頁面。
    顯示不同類別的小說排行榜。
    """
    try:
        # 依類別分組並顯示排行 (此處簡單列出所有小說依 views 排序)
        all_novels = Novel.query.order_by(Novel.views.desc()).all()
        return render_template('ranking.html', novels=all_novels)
    except Exception as e:
        print(f"排行榜載入失敗: {e}")
        return render_template('ranking.html', novels=[])
