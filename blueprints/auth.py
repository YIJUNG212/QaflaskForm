from flask import Blueprint,render_template,jsonify,redirect,url_for,session
from flask_mail import Message
from exts import mail,db
from flask import request

from werkzeug.security import generate_password_hash,check_password_hash#在flask中的加密法
import string
import random
from models import EmailCaptchaModel,UserModel
from .forms import RegisterForm,LoginForm #用.forms,因為不是同一層


bp=Blueprint("auth",__name__,url_prefix="/seflask/auth")

@bp.route("/captcha/email")#設定截取信箱號
def get_email_captcha():
    #以GET方法獲得變量
    email =request.args.get("email")
    #設置一個4倍的digits的0至9的資料list
    source=string.digits*4
    #從上述的資料list,隨機取不重複的4個數字
    captcha =random.sample(source,4)
    #重新拚接字符串
    captcha ="".join(captcha)
    #寄信的設置
    message =Message(subject="驗證碼測試",recipients=[email],body=f"您的驗證碼是:{captcha}")
    mail.send(message)
    #將資料存至資料庫
    email_captcha=EmailCaptchaModel(email=email,captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()
    return "將信箱及驗證碼存入資料庫success"
    
    
    
    
   
@bp.route("/login",methods=['GET','POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        form =LoginForm(request.form)
        if form.validate():
            email=form.email.data
            password=form.password.data
            #先看資料有沒有在資料庫
            user =UserModel.query.filter_by(email=email).first()
            if not user:
                print("郵箱在數據庫中不存在於")
                return redirect(url_for("auth.register"))
            
            else:#這裡是表示如果有帳號的話,才開始驗證密碼
                if check_password_hash(user.password,password):#順序不能錯亂
                    session['user_id']=user.id
                    
                    # return("密碼正確")
                    return redirect("/seflask/")
                else:
                    print("密碼錯誤")
                    return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return redirect(url_for("auth.login"))

@bp.route("/register",methods=['GET','POST'])
def register():
    if request.method == "GET":
        #一開始進來是先到視圖
        return  render_template("register.html")
    else:
        #當有POST方法才進到這個視圖
        form =RegisterForm(request.form)
        if form.validate():
            #驗證通過以後做的事
             #先要前端傳來的值,因為是用form.validate,所以有特有的取值方式
            email=form.email.data
            username =form.username.data
            password =form.password.data
            #取值完新增一個資料表的物件,密碼用哈希法生成,但哈希生成的套件要調用
            user =UserModel(email=email,username=username,password=generate_password_hash(password))
            #將物件增加及寫入
            db.session.add(user)
            db.session.commit()
            #執行後重新跳轉至目標,設定登入頁
            return  render_template("login.html")
            #return redirect(url_for("auth.login"))#跟上列同等效果
        else:
            print(form.errors)
            # return "fail"
            return redirect(url_for("auth.register"))
    

@bp.route("/mail/test")
def mail_test():
    message =Message(subject="郵箱測試",recipients=["poayung@gmail.com"],body="這是一個測試郵件")
    mail.send(message)
    return "郵件發送成功"

@bp.route("/logout")
def logout():
    session.clear()
    return redirect("/seflask")



# from flask import Flask, request, jsonify #上面已經import了
# 其他导入语句

# app = Flask(__name__) #這個不用,因為已經add到app.py去了

# 添加路由来处理删除旧验证码的请求
@bp.route('/delete_old_captcha', methods=['POST'])
def delete_old_captcha():
    email = request.json.get('email')
    # 在这里调用 deleteOldCaptcha 函数来删除旧验证码
    deleteOldCaptcha(email)
    return jsonify({'message': 'old data delete'})



# 导入数据库模型和相关库
#from models import EmailCaptchaModel #上面import了
from sqlalchemy import delete
import random

# 删除旧验证码的函数
def deleteOldCaptcha(email):
    # 使用 SQLAlchemy 执行删除操作，假设你的模型中有一个名为 CaptchaModel 的模型
    # 这里假设你的模型中有一个 email 字段用于匹配特定用户的验证码
    # 注意：以下代码只是示例，具体的删除操作需要根据你的数据库结构来实现
    delete_statement = delete(EmailCaptchaModel).where(EmailCaptchaModel.email == email)
    db.session.execute(delete_statement)
    db.session.commit()
    
    #應該也可以這麼寫
    #email_captcha=EmailCaptchaModel(email=email)
    #db.session.delete(email_captcha)
    #db.session.commit()

