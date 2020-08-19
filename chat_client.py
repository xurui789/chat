from socket import *
from multiprocessing import Process
import sys

address = ("0.0.0.0", 8888)


def login(udp_socket):
    while True:
        name = input("请输入姓名：")
        msg = "L " + name
        udp_socket.sendto(msg.encode(), address)
        data, addr = udp_socket.recvfrom(1024)
        if data.decode() == "登录成功":
            print("已经进入聊天室")
            return name
        else:
            print("换一个吧")


def chat_send(udp_socket, name):
    while True:
        msg = input("发送消息：")

        if msg == "exit":
            data = "E " + name
            udp_socket.sendto(data.encode(), address)
            sys.exit("已退出")
        data = "C %s %s" % (name, msg)
        udp_socket.sendto(data.encode(), address)


def chat_receive(udp_socket):
    while True:
        data, addr = udp_socket.recvfrom(1024)
        print("\n",data.decode()+"\n发送消息：",end="")


def main():
    udp_socket = socket(AF_INET, SOCK_DGRAM)
    name = login(udp_socket)
    p = Process(target=chat_receive, args=(udp_socket,))
    p.daemon = True
    p.start()
    chat_send(udp_socket, name)
    # udp_socket.close()


if __name__ == '__main__':
    main()
