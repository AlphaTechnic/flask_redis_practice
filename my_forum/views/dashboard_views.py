from flask import Blueprint, g
from flask_api import status

g_dashboard_size = 10

bp = Blueprint('dashboard', __name__, url_prefix='/')


@bp.route('/dashboard/', methods=['GET'])
def get_dashboard():
    def make_resp_body():
        body = dict()
        body["message"] = f"게시판마다 최대 {g_dashboard_size} 개의 post 조회 성공"
        body["data"] = dict()
        boards = g.user.boards.all()
        body["data"]["dashboardSize"] = len(boards)
        body["data"]["dashboardList"] = make_dashboard(boards)
        return body

    def make_dashboard(boards):
        arr_of_dashboard = []
        boards.sort(key=lambda board: board.create_date, reverse=True)
        for board in boards:
            dashboard = dict()
            dashboard["boardId"] = board.id
            dashboard["boardName"] = board.name
            posts = sorted(board.posts.all(), key=lambda post: post.create_date, reverse=True)[:g_dashboard_size]
            dashboard["posts"] = [{"id": post.id, "title": post.title} for post in posts]
            arr_of_dashboard.append(dashboard)
        return arr_of_dashboard

    body = make_resp_body()
    return body, status.HTTP_200_OK
