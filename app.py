from flask import Flask,session,g
import config
from exts import db,mail# 調用插件
from models import UserModel#調用資料表
from blueprints.qa import bp as qa_bp
from blueprints.auth import bp as auth_bp
from flask_migrate import Migrate

app =Flask(__name__)
app.config.from_object(config)
db.init_app(app)#將插件db重新綁定app主程式
mail.init_app(app)#將信箱套件綁定主程式
#migrate物件生成
migrate =Migrate(app,db)
#藍圖綁定
app.register_blueprint(qa_bp)
app.register_blueprint(auth_bp)
#視圖函式全部放到藍圖去了,所以不用在這裡寫了
# @app.route("/seflask")
# def index():
#     return "這是index"

#befor_request/befor_first_request/after_request

@app.before_request
def my_before_request():
    user_id=session.get("user_id")#這樣就算動透過flask 解析加密後的資料,解密返回
    if user_id:
        user =UserModel.query.get(user_id)#這個是得到整張表的物件
        setattr(g,"user",user)
    else:
        setattr(g,"user",None)

@app.context_processor
def my_context_processor():
    return {"user":g.user}


if __name__ == "__main__":
    app.run()

