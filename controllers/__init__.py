from models.Cookie import Cookie
from models.User import User
from utils import log, template


# 将 headers 作为参数传入是个很好的想法
def formatted_header(headers=None, status=200):
    d = {
        200: 'OK',
        302: 'Moved Permanently',
        404: 'NOT FOUND',
    }
    header = 'HTTP/1.1 {} {}\r\n'.format(
        status, d.get(status, 'OK')
    )
    if headers is not None:
        header += ''.join(
            ['{}: {}\r\n'.format(k, v) for k, v in headers.items()]
        )
    return header


def http_response(body, headers=None, status=200):
    header = formatted_header(headers, status)
    response = '{}\r\n{}'.format(header, body)
    return response.encode()


def redirect(path, headers=None):
    log('redirect to {}'.format(path))
    h = {
        'Location': path
    }
    if headers is not None:
        h.update(headers)
    response = http_response('', h, 302)
    return response


def current_user(request):
    session_id = request.cookies.get('session_id', '')
    cookie = Cookie.find_by(session_id=session_id)
    if cookie is not None:
        user = User.find_by(id=cookie.user_id)
        log('current user: {}'.format(user.username))
        return user
    else:
        log('current user: None')
        return None


def login_required(route_function):
    def wrapper(request):
        user = current_user(request)
        if user is None:
            return redirect('/login')
        else:
            return route_function(request)

    return wrapper


def error(request):
    body = '<h1>404 NOT FOUND</h1>'
    response = http_response(body, None, 404)
    return response
