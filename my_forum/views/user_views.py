from flask import Blueprint, request, session
from flask_api import FlaskAPI, status

from my_forum.forms import UserCreateForm, UserLoginForm
from my_forum.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from my_forum import db

bp = Blueprint('user', __name__, url_prefix='/')


@bp.route('/signup/', methods='POST')
def signup():
    def make_resp(success):
        resp = dict()
        resp["data"] = {}
        if success:
            resp["message"] = "가입 성공"
        else:
            resp["message"] = "이미 가입된 메일"
        return resp

    def create_user(form):
        user = User(
            username=form.username.data,
            password=generate_password_hash(form.password.data),
            email=form.email.data
        )
        db.session.add(user)
        db.session.commit()

    form = UserCreateForm()
    # flash(form.errors)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            create_user(form)
            resp = make_resp(success=True)
            return resp, status.HTTP_200_OK
        resp = make_resp(success=False)
        return resp, status.HTTP_409_CONFLICT

    return {"message": "유효하지 않은 요청"}, status.HTTP_400_BAD_REQUEST


@bp.route('/login/', methods='POST')
def login():
    def make_resp(user_in_db, valid_password=True):
        resp = dict()
        resp["data"] = {}
        if user_in_db and valid_password:
            resp["message"] = "로그인 성공"
        elif user_in_db and not valid_password:
            resp["message"] = "유효하지 않은 password"

        resp["message"] = "존재하지 않는 사용자"
        return resp

    form = UserLoginForm()
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(username=form.email.data).first()
        if not user:
            resp = make_resp(user_in_db=False)
            return resp, status.HTTP_404_NOT_FOUND
        elif not check_password_hash(user.password, form.password.data):
            resp = make_resp(user_in_db=True, valid_password=False)
            return resp, status.HTTP_400_BAD_REQUEST

        session.clear()
        session['user_id'] = user.id
        resp = make_resp(user_in_db=True, valid_password=True)
        return resp, status.HTTP_200_OK

    return {"message": "유효하지 않은 요청"}, status.HTTP_400_BAD_REQUEST

