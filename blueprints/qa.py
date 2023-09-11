from flask import Blueprint,request,render_template,g,redirect,url_for
from .forms import QuestionForm,AnswerForm
from exts import db
from models import QuestionModel,AnserModel
from decorators import login_required#  調用客制化裝飾器
bp=Blueprint("qa",__name__,url_prefix="/seflask")
@bp.route("/")
def index():
    questions=QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()#用創造成時間來排序,拿出所有資料
    return render_template("index.html",questions=questions)#將變數以questions的索引傳入視圖

@bp.route("/qa/public",methods=['GET','POST'])
@login_required
def public_question():
    if request.method == "GET":
        return render_template("public_question.html")
    else:
        form =QuestionForm(request.form)
        if form.validate():
            title =form.title.data
            content =form.content.data
            question =QuestionModel(title=title,content=content,author=g.user)
            db.session.add(question)
            db.session.commit()
            return redirect("/seflask")
        else:
            print(form.errors)
            return redirect(url_for("qa.public_question"))
@bp.route("/qa/detail/<qa_id>")
def qa_detail(qa_id):
    question=QuestionModel.query.get(qa_id)
    if question:
        return render_template("detail.html",question=question)
    else:
        return "資料不存在"


# @bp.route("/answer/public",methods=['POST'])
@bp.post("/answer/public")
@login_required
def public_answer():
    form =AnswerForm(request.form)
    if form.validate():
        content = form.content.data
        question_id =form.question_id.data
        answer =AnserModel(content=content,question_id=question_id,author_id=g.user.id)
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for("qa.qa_detail",qa_id=question_id))
    else:
        print(form.errors)
        return redirect(url_for("qa.qa_detail",qa_id=request.form.get("question_id")))

@bp.route("/search")
def search():
    q=request.args.get("q")
    questions=QuestionModel.query.filter(QuestionModel.title.contains(q)).all()
    return render_template("index.html",questions=questions)