from flask import Blueprint, request, session, make_response, jsonify, g, redirect, url_for
from flask_api import status
from .validation import is_authenticated

from my_forum.forms import UserCreateForm, UserLoginForm
from my_forum.models import User, Board
from werkzeug.security import generate_password_hash, check_password_hash
from my_forum import db
from datetime import datetime, timedelta

g_board_page_size = 5
g_post_page_size = 10

bp = Blueprint('board', __name__, url_prefix='/')


@bp.route('/board/', methods=['POST', 'PATCH', 'DELETE'])
def handle_board():
    if request.method == 'POST':
        board_name = request.get_json()['name']
        board = Board(user_id=g.user.id, name=board_name, create_date=datetime.now())

        db.session.add(board)
        db.session.commit()
        return {"message": f"[{board_name}] 생성 성공", "data": {}}, status.HTTP_201_CREATED

    if request.method == 'PATCH':
        board_id_to_delete = request.get_json()['id']
        if not is_authenticated(board_id_to_delete):
            return {"message": "수정 권한 없음", "data": {}}, status.HTTP_403_FORBIDDEN

        board_name = request.get_json()['name']
        board = Board.query.get(board_id_to_delete)

        prev_name = board.name
        board.name = board_name

        db.session.add(board)
        db.session.commit()
        return {"message": f"[{prev_name}]->[{board_name}] 수정 성공", "data": {}}, status.HTTP_200_OK

    if request.method == 'DELETE':
        id_to_delete = request.get_json()['id']
        if not is_authenticated(id_to_delete):
            return {"message": "삭제 권한 없음", "data": {}}, status.HTTP_403_FORBIDDEN
        board = Board.query.get(id_to_delete)
        name_to_delete = board.name

        db.session.delete(board)
        db.session.commit()
        return {"message": f"[board{id_to_delete}/{name_to_delete}] 삭제 성공", "data": {}}, status.HTTP_200_OK

    return {"message": "유효하지 않은 요청", "data": {}}, status.HTTP_400_BAD_REQUEST


@bp.route('/boards/', methods=['GET'])
def get_boards():
    def make_resp_body(user):
        body = dict()
        body["message"] = "게시판 목록들 요청 성공"
        body["data"] = dict()
        body["data"]["limit"] = g_board_page_size
        body["data"]["pages"] = make_pages(user)
        return body

    def make_pages(user):
        boards = user.boards.all()
        boards.sort(key=lambda board: board.create_date, reverse=True)

        pages = list()
        page_num = 1
        start_idx = 0
        while True:
            end_idx = make_page(boards, page_num, pages, start_idx)
            if end_idx >= len(boards):
                break
            start_idx = end_idx
            page_num += 1
        return pages

    def make_page(boards, page_num, pages, start):
        page = dict()
        page["page_num"] = page_num
        page["offset"] = start
        end = start + g_board_page_size * page_num
        page["boards"] = [{"id": board.id, "name": board.name} for board in boards[start: end]]
        pages.append(page)
        return end

    if request.method == "GET":
        resp = make_resp_body(g.user)
        return resp, status.HTTP_200_OK
    return {"message": "유효하지 않은 요청", "data": {}}, status.HTTP_400_BAD_REQUEST


@bp.route('/board/<int:board_id>/articles/', methods=['GET'])
def get_posts(board_id):
    def make_resp_body(board):
        body = dict()
        body["message"] = "post 목록들 요청 성공"
        body["data"] = dict()
        body["data"]["limit"] = g_post_page_size
        body["data"]["pages"] = make_pages(board)
        return body

    def make_pages(board):
        posts = board.posts.all()
        posts.sort(key=lambda board: board.create_date, reverse=True)

        pages = list()
        page_num = 1
        start_idx = 0
        while True:
            end_idx = make_page(posts, page_num, pages, start_idx)
            if end_idx >= len(posts):
                break
            start_idx = end_idx
            page_num += 1
        return pages

    def make_page(posts, page_num, pages, start):
        page = dict()
        page["page_num"] = page_num
        page["offset"] = start
        end = start + g_post_page_size * page_num
        page["posts"] = [{"id": post.id, "title": post.title} for post in posts]
        pages.append(page)
        return end

    if request.method == "GET":
        if is_authenticated(board_id):
            return {"message": "조회 권한 없음", "data": {}}, status.HTTP_403_FORBIDDEN
        board = Board.query.get(board_id)
        resp = make_resp_body(board)
        return resp, status.HTTP_200_OK

    return {"message": "유효하지 않은 요청", "data": {}}, status.HTTP_400_BAD_REQUEST
