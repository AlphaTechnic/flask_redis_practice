from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class UserCreateForm(FlaskForm):
    username = StringField("아이디",
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("이메일",
                        validators=[DataRequired(), Email()])
    password = PasswordField("비밀번호",
                             validators=[DataRequired(), Length(min=4, max=20)])
    confirm_password = PasswordField("비밀번호 확인",
                                     validators=[DataRequired(), EqualTo("password")])

    # username = StringField("아이디")
    # email = StringField("이메일")
    # password = PasswordField("비밀번호")
    # confirm_password = PasswordField("비밀번호확인")
