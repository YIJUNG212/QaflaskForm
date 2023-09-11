import wtforms
from wtforms.validators import Email,Length,EqualTo,InputRequired
from models import UserModel,EmailCaptchaModel

class RegisterForm(wtforms.Form):
    #底下是設定各個form的input格式，不管前端有沒有限制，這裡都可以把關
    email =wtforms.StringField(validators=[Email(message="郵箱格式錯誤")])
    captcha =wtforms.StringField(validators=[Length(min=4,max=4,message="驗證碼格式錯誤!")])
    username =wtforms.StringField(validators=[Length(min=3,max=20,message="用戶名格式錯誤!")])
    password =wtforms.StringField(validators=[Length(min=6,max=20,message="密碼格式錯誤!")])
    password_confirm =wtforms.StringField(validators=[EqualTo("password",message="兩次密碼不相同")])
    #以下自定義驗證
    def validate_email(self, field):
        email=field.data
        #檢查正要新增的email與資料庫內有無相同值
        user=UserModel.query.filter_by(email=email).first()
        #若存在
        if user:
            raise wtforms.ValidationError(message="該郵箱已經被註冊!")
        else:
            #若不存在,就新增進UserModel資料庫吧
            pass
    def validate_captcha(self, field):
        #理論上要執行這邊的表格檢查時，信箱及驗證碼應該已經在資料庫了，所以當按下form的commit鈕時，應該可以有相對應的驗證碼及信箱
        captcha =field.data
        email=self.email.data
        captcha_model=EmailCaptchaModel.query.filter_by(email=email,captcha=captcha).first()
        if not captcha_model:
            raise wtforms.ValidationError(message="郵箱或驗證碼錯誤!")

class LoginForm(wtforms.Form):
    #底下是設定各個form的input格式，不管前端有沒有限制，這裡都可以把關
    email =wtforms.StringField(validators=[Email(message="郵箱格式錯誤")])
    password =wtforms.StringField(validators=[Length(min=6,max=20,message="密碼格式錯誤!")])

class QuestionForm(wtforms.Form):
    #底下是設定各個form的input格式，不管前端有沒有限制，這裡都可以把關
    title =wtforms.StringField(validators=[Length(min=3,max=100,message="標題格式錯誤!")])
    content =wtforms.StringField(validators=[Length(min=3,message="內容格式錯誤!")])

class AnswerForm(wtforms.Form):
    content =wtforms.StringField(validators=[Length(min=3,message="內容格式錯誤!")])
    question_id =wtforms.IntegerField(validators=[InputRequired(message="必須要傳入問題id")])