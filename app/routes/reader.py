from flask import Blueprint, render_template, request, redirect, url_for, session
from app.models.novel import Novel, Chapter
from app.models.record import Record, Collection

reader_bp = Blueprint('reader', __name__)

@reader_bp.route('/novel/<int:novel_id>')
def detail(novel_id):
    """
    小說詳情頁。
    """
    novel = Novel.get_by_id(novel_id)
    if not novel:
        flash('找不到該小說。', 'danger')
        return redirect(url_for('main.index'))
    
    # 增加點擊數
    novel.update(views=novel.views + 1)
    
    return render_template('novel/detail.html', novel=novel)

@reader_bp.route('/novel/<int:novel_id>/read/<int:chapter_num>')
def read(novel_id, chapter_num):
    """
    閱讀介面。
    """
    novel = Novel.get_by_id(novel_id)
    chapters = Chapter.get_by_novel_id(novel_id)
    
    # 找尋特定序號的章節
    chapter = next((c for c in chapters if c.chapter_num == chapter_num), None)
    
    if not chapter:
        flash('找不到該章節。', 'warning')
        return redirect(url_for('reader.detail', novel_id=novel_id))
    
    # 如果使用者已登入，更新閱讀紀錄
    if 'user_id' in session:
        Record.create_or_update(user_id=session['user_id'], novel_id=novel_id, last_chapter_id=chapter.id)
    
    return render_template('novel/reader.html', novel=novel, chapter=chapter, chapters=chapters)

@reader_bp.route('/novel/<int:novel_id>/collect', methods=['POST'])
def collect(novel_id):
    """
    收藏操作。
    """
    if 'user_id' not in session:
        flash('請先登入以使用收藏功能。', 'warning')
        return redirect(url_for('auth.login'))
        
    action = request.form.get('action') # 'add' or 'remove'
    if action == 'add':
        Collection.add(user_id=session['user_id'], novel_id=novel_id)
        flash('已加入收藏。', 'success')
    elif action == 'remove':
        Collection.remove(user_id=session['user_id'], novel_id=novel_id)
        flash('已從收藏移除。', 'info')
        
    return redirect(url_for('reader.detail', novel_id=novel_id))

@reader_bp.route('/profile')
def profile():
    """
    個人中心 (我的書架)。
    """
    if 'user_id' not in session:
        flash('請先登入。', 'warning')
        return redirect(url_for('auth.login'))
        
    user_id = session['user_id']
    records = Record.get_by_user(user_id)
    collections = Collection.get_by_user(user_id)
    
    return render_template('profile.html', records=records, collections=collections)
