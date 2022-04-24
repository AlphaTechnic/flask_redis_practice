from flask import Blueprint, request, session, make_response, jsonify, g, redirect, url_for
from flask_api import FlaskAPI, status

from my_forum.forms import UserCreateForm, UserLoginForm
from my_forum.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from my_forum import db
from datetime import datetime, timedelta

bp = Blueprint('user', __name__, url_prefix='/')


@bp.before_app_request
def load_logged_in_user():
    allowed_routes = ['user.signup', 'user.login']
    if request.endpoint in allowed_routes:
        return

    email = session.get('session_id')
    if email is None:
        g.user = None
        return redirect(url_for('user.login'))
    else:
        g.user = User.query.filter_by(email=email).first()


@bp.route('/signup/', methods=['POST'])
def signup():
    def make_resp_body(success):
        body = dict()
        body["data"] = {}
        if success:
            body["message"] = "가입 성공"
        else:
            body["message"] = "이미 가입된 메일"
        return body

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
        # user = db.session.query(User).filter_by(email=form.email.data).first()
        if not user:
            create_user(form)
            body = make_resp_body(success=True)
            return body, status.HTTP_200_OK
        body = make_resp_body(success=False)
        return body, status.HTTP_409_CONFLICT

    return {"message": "유효하지 않은 요청"}, status.HTTP_400_BAD_REQUEST


@bp.route('/login/', methods=['GET', 'POST'])
def login():
    def make_resp_body(user_in_db, valid_password=True):
        body = dict()
        body["data"] = {}
        if user_in_db:
            if valid_password:
                body["message"] = "로그인 성공"
            else:
                body["message"] = "유효하지 않은 password"
            return body

        body["message"] = "존재하지 않는 사용자"
        return body

    def save_in_server_session(user):
        session.clear()
        session['session_id'] = user.email

    def response_with_cookie(user):
        body = make_resp_body(user_in_db=True, valid_password=True)
        response = make_response(jsonify(body), status.HTTP_200_OK)

        expire_time = datetime.now() + timedelta(days=1)
        response.set_cookie("session_id", value=user.email, expires=expire_time, httponly=True)
        return response

    if request.method == 'GET':
        return {"message": "로그인 화면"}, status.HTTP_200_OK

    form = UserLoginForm()
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            body = make_resp_body(user_in_db=False)
            return body, status.HTTP_404_NOT_FOUND
        elif not check_password_hash(user.password, form.password.data):
            body = make_resp_body(user_in_db=True, valid_password=False)
            return body, status.HTTP_400_BAD_REQUEST

        save_in_server_session(user)
        response = response_with_cookie(user)
        return response

    return {"message": "유효하지 않은 요청"}, status.HTTP_400_BAD_REQUEST


@bp.route('/logout/', methods=['GET'])
def logout():
    session.clear()
    return {"message": "로그아웃 성공"}, status.HTTP_200_OK
