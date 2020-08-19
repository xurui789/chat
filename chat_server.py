from socket import *
from multiprocessing import Process

user = {}

addr = ("127.0.0.1", 8888)
def login(udp_socket, name, addr):
    if name in user or "管理员" in name:
        udp_socket.sendto("姓名不能重复：".encode(), addr)
        return
    else:
        udp_socket.sendto("登录成功".encode(), addr)
        msg = "%s进入聊天室" % name
        for i in user:
            udp_socket.sendto(msg.encode(), user[i])
        user[name] = addr


def chat(udp_socket, name, content):
    msg = "%s:%s" % (name, content)
    for i in user:
        if i != name:
            udp_socket.sendto(msg.encode(), user[i])


def exit(udp_socket, name):
    del user[name]
    msg = "%s退出聊天室"%name
    for i in user:
        udp_socket.sendto(msg.encode(), user[i])


def handle(udp_socket):
    while True:
        data, addr = udp_socket.recvfrom(1024)
        tmp = data.decode().split(" ", 2)
        if tmp[0] == 'L':
            login(udp_socket, tmp[1], addr)
        elif tmp[0] == 'C':
            chat(udp_socket, tmp[1], tmp[2])
        elif tmp[0] == 'E':
            exit(udp_socket, tmp[1])


def main():
    udp_socket = socket(AF_INET, SOCK_DGRAM)

    udp_socket.bind(addr)
    p = Process(target=handle, args=(udp_socket,))
    p.daemon = True
    p.start()
    while True:
        content = input("管理员消息：")
        if content == "quit":
            break
        data = "C 管理员消息 " + content
        udp_socket.sendto(data.encode(), ("127.0.0.1", 8888))
    # udp_socket.close()


if __name__ == '__main__':
    main()
