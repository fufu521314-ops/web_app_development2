import os
from flask import Flask
from app.models import db

def create_app(test_config=None):
    # 建立與設定 Flask App
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.instance_path, 'database.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config is None:
        # 載入實體設定 (如果有的話)
        app.config.from_pyfile('config.py', silent=True)
    else:
        # 載入測試設定
        app.config.from_mapping(test_config)

    # 確保實體資料夾存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 初始化資料庫
    db.init_app(app)

    # 註冊 Blueprints
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.reader import reader_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(reader_bp)

    return app

def init_db():
    app = create_app()
    with app.app_context():
        db.create_all()
        print("資料庫已初始化。")
