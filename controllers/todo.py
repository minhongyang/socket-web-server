import time

from controllers import current_user, http_response, redirect, login_required
from models.Todo import Todo
from utils import template, log, formatted_time


def index(request):
    user = current_user(request)
    todo_list = Todo.find_all(user_id=user.id)
    body = template('todo.html', user=user.username, todo_list=todo_list)

    return http_response(body)


def add(request):
    user = current_user(request)
    if request.method == 'POST':
        form = dict(
            user_id=user.id,
            username=user.username,
            task=request.body.get('todo_task', ''),
        )
        Todo.new(form)
    return redirect('/todo')


def edit(request):
    todo_id = int(request.query.get('id', None))
    todo = Todo.find_by(id=todo_id)
    body = template('todo_edit.html', todo=todo)
    return http_response(body)


def update(request):
    todo_id = int(request.query.get('id', None))
    form = request.body
    form.update(dict(
        updated_time=int(time.time())
    ))
    Todo.update(todo_id, form)
    return redirect('/todo')


def delete(request):
    todo_id = int(request.query.get('id'))
    log('delete todo id={}'.format(todo_id))
    Todo.delete(id=todo_id)
    return redirect('/todo')


def owner_required(route_function):
    def wrapper(request):
        user = current_user(request)
        todo_id = int(request.query.get('id'))
        todo = Todo.find_by(id=todo_id)
        if user.id == todo.user_id:
            return route_function(request)
        else:
            return redirect('/login')

    return wrapper


def todo_route():
    d = {
        '/todo': login_required(index),
        '/todo/add': login_required(add),
        '/todo/delete': login_required(owner_required(delete)),
        '/todo/edit': login_required(owner_required(edit)),
        '/todo/update': login_required(owner_required(update)),
    }
    return d
