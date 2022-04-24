from my_forum import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    # 다른 테이블과의 관계
    posts = db.relationship('Post', backref='user', lazy='dynamic')

    def __repr__(self):
        return f"user{self.id}/{self.username[:10]}"


class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)

    # 다른 테이블과의 관계
    posts = db.relationship('Post', backref='board', lazy='dynamic')

    def __repr__(self):
        return f"board{self.id}/{self.name[:10]}"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)

    # 다른 테이블과의 관계
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    board_id = db.Column(db.Integer, db.ForeignKey('board.id', ondelete='CASCADE'))

    def __repr__(self):
        return f"{self.board}->post{self.id}/{self.title[:10]}"
