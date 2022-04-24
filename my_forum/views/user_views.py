from flask import Blueprint, request, flash
from flask_api import FlaskAPI, status

from my_forum.forms import UserCreateForm
from my_forum.models import User
from werkzeug.security import generate_password_hash
from my_forum import db, csrf

bp = Blueprint('user', __name__, url_prefix='/')
# csrf.exempt(bp)


@bp.route('/signup/', methods=('GET', 'POST'))
# @csrf.exempt
def signup():
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

    return {"message": "INTERNAL_SERVER_ERROR"}, status.HTTP_500_INTERNAL_SERVER_ERROR


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


@bp.route('/')
def index():
    return 'Pybo index'
