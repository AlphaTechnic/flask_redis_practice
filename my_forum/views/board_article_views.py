from flask import Blueprint, request
from flask_api import status
from my_forum.validation import is_authenticated

from my_forum.models import Post
from my_forum import db
from datetime import datetime

bp = Blueprint('board_article', __name__, url_prefix='/')


@bp.route('/board/<int:board_id>/', methods=['POST'])
def create_post(board_id):
    if not is_authenticated(board_id):
        return {"message": "권한 없음", "data": {}}, status.HTTP_403_FORBIDDEN

    if request.method == 'POST':
        post_title = request.get_json()['title']
        post_content = request.get_json()['content']
        post = Post(board_id=board_id, title=post_title, content=post_content, create_date=datetime.now())

        db.session.add(post)
        db.session.commit()
        return {"message": "게시글 생성 성공", "data": {}}, status.HTTP_201_CREATED


@bp.route('/post/<int:post_id>/', methods=['GET', 'PATCH', 'DELETE'])
def handle_post(post_id):
    post = Post.query.get(post_id)
    if post is None or not is_authenticated(post.board.id):
        return {"message": "권한 없음", "data": {}}, status.HTTP_403_FORBIDDEN

    if request.method == 'GET':
        post = Post.query.get(post_id)
        return {"message": "게시글 조회 성공", "data": {"title": f"{post.title}"}}, status.HTTP_200_OK

    if request.method == 'PATCH':
        new_title = request.get_json()['title']
        new_content = request.get_json()['content']
        post = Post.query.get(post_id)

        prev_title = post.title
        post.title = new_title
        post.content = new_content

        db.session.add(post)
        db.session.commit()
        return {"message": f"[{prev_title}]->[{post.title}] 게시글 수정 성공", "data": {}}, status.HTTP_200_OK

    if request.method == 'DELETE':
        post = Post.query.get(post_id)
        db.session.delete(post)
        db.session.commit()
        return {"message": f"[{post.title}] 게시글 삭제 성공", "data": {}}, status.HTTP_200_OK

    return {"message": "유효하지 않은 요청", "data": {}}, status.HTTP_400_BAD_REQUEST
