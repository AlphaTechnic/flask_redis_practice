from flask import Blueprint, request, g
from flask_api import status
from my_forum.validation import is_authenticated

from my_forum.models import Board
from my_forum import db
from datetime import datetime

g_board_page_size = 5
g_post_page_size = 10

bp = Blueprint('board', __name__, url_prefix='/')


@bp.route('/board/', methods=['POST'])
def create_board():
    if request.method == 'POST':
        board_name = request.get_json()['name']
        board = Board(user_id=g.user.id, name=board_name, create_date=datetime.now())

        db.session.add(board)
        db.session.commit()
        return {"message": f"[{board_name}] 생성 성공", "data": {}}, status.HTTP_201_CREATED
    return {"message": "유효하지 않은 요청", "data": {}}, status.HTTP_400_BAD_REQUEST


@bp.route('/board/<int:board_id>/', methods=['GET', 'PATCH', 'DELETE'])
def handle_specific_post(board_id):
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
        page["pageNum"] = page_num
        page["offset"] = start
        end = start + g_post_page_size * page_num
        page["posts"] = [{"id": post.id, "title": post.title} for post in posts]
        pages.append(page)
        return end

    if request.method == "GET":
        board = Board.query.get(board_id)
        if not is_authenticated(board_id):
            return {"message": "조회 권한 없음", "data": {}}, status.HTTP_403_FORBIDDEN
        board = Board.query.get(board_id)
        resp = make_resp_body(board)
        return resp, status.HTTP_200_OK

    if request.method == 'DELETE':
        if not is_authenticated(board_id):
            return {"message": "삭제 권한 없음", "data": {}}, status.HTTP_403_FORBIDDEN
        board = Board.query.get(board_id)
        name_to_delete = board.name

        db.session.delete(board)
        db.session.commit()
        return {"message": f"[board{board_id}/{name_to_delete}] 삭제 성공", "data": {}}, status.HTTP_200_OK

    if request.method == 'PATCH':
        if not is_authenticated(board_id):
            return {"message": "수정 권한 없음", "data": {}}, status.HTTP_403_FORBIDDEN

        board_name = request.get_json()['name']
        board = Board.query.get(board_id)
        prev_name = board.name
        board.name = board_name

        db.session.add(board)
        db.session.commit()
        return {"message": f"[{prev_name}]->[{board_name}] 수정 성공", "data": {}}, status.HTTP_200_OK

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
