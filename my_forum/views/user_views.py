from flask import Blueprint, request, session, make_response, jsonify
from flask_api import FlaskAPI, status

from my_forum.forms import UserCreateForm, UserLoginForm
from my_forum.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from my_forum import db

bp = Blueprint('user', __name__, url_prefix='/')


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


@bp.route('/login/', methods=['POST'])
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
        session['user_id'] = user.email

    def response_with_cookie(user):
        body = make_resp_body(user_in_db=True, valid_password=True)
        response = make_response(jsonify(body), status.HTTP_200_OK)
        response.set_cookie("user_id", value=user.email)
        return response

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
