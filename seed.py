from app import create_app
from app.models import db
from app.models.novel import Novel, Chapter
from werkzeug.security import generate_password_hash
from app.models.user import User

app = create_app()

with app.app_context():
    # 建立測試使用者
    if not User.get_by_username('testuser'):
        User.create(username='testuser', password_hash=generate_password_hash('password123'), email='test@example.com')
        print("測試使用者已建立。")

    # 建立測試小說
    if not Novel.query.first():
        n1 = Novel.create(title='三國演義', author='羅貫中', description='天下大勢，合久必分，分久必合。', category='歷史')
        n2 = Novel.create(title='西遊記', author='吳承恩', description='唐三藏西天取經的故事。', category='神魔')
        n3 = Novel.create(title='水滸傳', author='施耐庵', description='梁山好漢的故事。', category='冒險')
        
        # 建立章節
        Chapter.create(novel_id=n1.id, title='第一回：宴桃園豪傑三結義', content='話說天下大勢，合久必分，分久必合...', chapter_num=1)
        Chapter.create(novel_id=n1.id, title='第二回：張翼德怒鞭督郵', content='話說曹操字孟德，沛國譙人也...', chapter_num=2)
        
        Chapter.create(novel_id=n2.id, title='第一回：靈根育孕源流出', content='混沌未分天地亂，茫茫渺渺無人見...', chapter_num=1)
        
        print("測試小說與章節已建立。")
