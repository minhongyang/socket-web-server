"""
构建流程：
1. 实现循环接收请求（不处理），返回默认响应的基本功能
2. 将代码封装成函数，host 和 port 作为参数
3. 解析 client 的请求
4. 添加 index 页面和路由函数，响应的主页路由函数和其中图片的路由函数
5. 重构路由函数，将其分离并集中到 controller 中
6. 创建一个 request 类，方便调用属性，重构 server，加入多线程处理请求响应
7. 添加 register 页面和路由函数，增加 user 类到 model 中，实现数据保存
8. 重构类函数，将通用类方法提炼到一个超类中
9. 添加 login 页面和路由函数，实现伪登陆
10. 添加 cookie 功能，利用 session_id 验证用户身份
11. 添加 todo 页面和路由函数，包含重定向相关函数
12. 为 todo 增加增删改查功能
13. 重构函数，将身份验证等功能提炼出来
14. 引入 jinja2 模板
15. 密码保存由明文改为 Hash 值
16. 将路由模块拆分,增加 weibo 页面和路由函数
17. 增加修改密码功能
"""
import socket
import _thread

from models.Request import Request
from utils import log
from controllers import error
from controllers.static import static_route
from controllers.user import user_route
from controllers.todo import todo_route
from controllers.weibo import weibo_route


def request_by_socket(connection):
    request = b''
    buffer_size = 1024
    while True:
        r = connection.recv(buffer_size)
        request += r
        if len(r) < buffer_size:
            return request.decode()


def response_by_request(request):
    r = Request()
    r.parsed_request(request)
    route = {}
    route.update(static_route())
    route.update(user_route())
    route.update(todo_route())
    route.update(weibo_route())
    response = route.get(r.path, error)
    return response(r)


def process_request(connection):
    # 通过连接接收请求
    request = request_by_socket(connection)

    # 通过连接发送响应
    response = response_by_request(request)
    log('response:', response)
    connection.sendall(response)

    # 收发数据结束，关闭连接，或者整体用 with 包起来
    connection.close()


def run(host, port):
    # 创建 socket 对象
    log('开始运行于', '{}:{}'.format(host, port))
    with socket.socket() as s:
        # 使用 下面这句 可以保证程序重启后使用原有端口, 原因忽略
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 设置 socket 的属性
        s.bind((host, port))

        # 让 socket 进入监听状态
        s.listen()

        while True:
            # 监听到 client 的连接请求
            # 接收 client 的连接请求数据
            # 并创建一个新的 socket(变量 connection 是 socket object)，与该 client 建立连接
            # 用于监听的 socket 继续原来的工作，监听其他 client 的连接请求
            connection, address = s.accept()
            # log('client address:', address)

            # 多线程处理请求
            _thread.start_new_thread(process_request, (connection, ))


if __name__ == '__main__':
    config = dict(
        host='0.0.0.0',
        port=3000,
    )
    run(**config)
