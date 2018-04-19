from controllers import current_user, http_response
from models.User import User
from utils import template


def index(request):
    user = current_user(request)
    users = User.all()
    if user is None:
        body = template('index.html', user='游客', users=users)
    else:
        body = template('index.html', user=user.username, users=users)

    return http_response(body)


def static(request):
    header = b'HTTP/1.1 200 GET PIC\r\n\r\n'
    file_path = 'static/{}'.format(request.query.get('file'))
    with open(file_path, 'rb') as file:
        body = file.read()
    response = header + body
    return response


def static_route():
    d = {
        '/': index,
        '/static': static,
    }
    return d
