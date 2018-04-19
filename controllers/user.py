from controllers import redirect, http_response, formatted_header, current_user, login_required
from models.Cookie import Cookie
from models.User import User
from utils import template, random_string, log


def register(request):
    if request.method == 'POST':
        user = User(request.body)
        if user.valid_register():
            user.save()
            return redirect('/login')
        else:
            body = template('register.html', result='用户名已存在')
    else:
        body = template('register.html', result='请输入如下信息')

    return http_response(body)


def login(request):
    if request.method == 'POST':
        user = User(request.body)
        if user.valid_login():
            u = User.find_by(username=user.username)
            form = dict(
                user_id=u.id,
                username=u.username,
                session_id=random_string(),
            )
            Cookie.new(form)
            headers = {
                'Set-Cookie': 'session_id={}'.format(form['session_id'])
            }
            return redirect('/', headers)
        else:
            body = template('login.html', user='登陆失败')
    else:
        body = template('login.html', user='游客')

    return http_response(body)


def setting(request):
    user = current_user(request)
    body = template('setting.html', user=user)
    return http_response(body)


def pwd_update(request):
    u = User(request.body)
    new_password = request.body.get('new_password')
    if u.valid_login():
        user = User.find_by(username=u.username)
        user.password = User.hashed_password(new_password)
        user.save()
        return redirect('/')
    else:
        body = template('setting.html', user=u, result='Old password is wrong')
        return http_response(body)


def user_route():
    d = {
        '/register': register,
        '/login': login,
        '/setting': login_required(setting),
        '/password/update': login_required(pwd_update),
    }
    return d
