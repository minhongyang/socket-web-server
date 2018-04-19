from controllers import http_response, current_user, redirect, login_required
from models.Comment import Comment
from models.Weibo import Weibo
from utils import template


def index(request):
    user_id = int(request.query.get('user_id'))
    weibos = Weibo.find_all(user_id=user_id)
    body = template('weibo.html', user_id=user_id, weibos=weibos)
    return http_response(body)


def add(request):
    user = current_user(request)
    user_id = int(request.body.get('user_id'))
    if request.method == 'POST' and user.id == user_id:
        form = dict(
            user_id=user_id,
            username=user.username,
            content=request.body.get('content'),
        )
        Weibo.new(form)
    return redirect('/weibo?user_id={}'.format(user_id))


def delete(request):
    weibo_id = int(request.query.get('id'))
    weibo = Weibo.find_by(id=weibo_id)
    weibo.delete_comments()
    Weibo.delete(id=weibo_id)
    user_id = weibo.user_id
    return redirect('/weibo?user_id={}'.format(user_id))


def edit(request):
    weibo_id = int(request.query.get('id'))
    weibo = Weibo.find_by(id=weibo_id)
    body = template('weibo_edit.html', weibo=weibo)
    return http_response(body)


def update(request):
    weibo_id = int(request.query.get('id', None))
    weibo = Weibo.find_by(id=weibo_id)
    weibo.update(weibo_id, request.body)
    user_id = weibo.user_id
    return redirect('/weibo?user_id={}'.format(user_id))


def comment(request):
    user = current_user(request)
    weibo_id = int(request.query.get('id'))
    form = dict(
        user_id=user.id,
        weibo_id=weibo_id,
        username=user.username,
        content=request.body.get('content'),
    )
    Comment.new(form)
    weibo = Weibo.find_by(id=weibo_id)
    user_id = weibo.user_id
    return redirect('/weibo?user_id={}'.format(user_id))


def owner_required(route_function):
    def wrapper(request):
        user = current_user(request)
        weibo_id = int(request.query.get('id'))
        weibo = Weibo.find_by(id=weibo_id)
        if user.id == weibo.user_id:
            return route_function(request)
        else:
            return redirect('/login')

    return wrapper


def weibo_route():
    d = {
        '/weibo': index,
        '/weibo/add': login_required(add),
        '/weibo/delete': login_required(owner_required(delete)),
        '/weibo/edit': login_required(owner_required(edit)),
        '/weibo/update': login_required(owner_required(update)),
        '/weibo/comment': login_required(comment),
    }
    return d
