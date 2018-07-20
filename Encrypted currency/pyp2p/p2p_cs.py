# ===========================================
# @Time    : 2018/5/11 14:31
# @Author  : antony
# @Email   : 502202879@qq.com
# @File    : gevent_cs.py
# @Software: PyCharm Community Edition
# ===========================================

import gevent
import socket
from gevent import socket, monkey, server
# monkey.patch_all()

# urls = ['www.baidu.com', 'www.gevent.org', 'www.python.org']
# jobs = [gevent.spawn(socket.gethostbyname, url) for url in urls]
# gevent.joinall(jobs, timeout=5)
#
# print([job.value for job in jobs])


class UdpSocket():
    def __init__(self, l_addr, timeout=None):
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.soc.bind(l_addr)
        if timeout:
            self.soc.settimeout(timeout)

    def send_message(self, message, addr):
        self.soc.sendto(message.encode(), addr)

    def recv_handle(self, hadle_func=print):
        try:
            hadle_func(self.soc, self.soc.recvfrom(1024,))
        except Exception as err:
            print(err)

    def listen_bytimes(self, times):
        for i in range(times):
            self.recv_handle(udp_handle_func)


def udp_handle_func(soc, mess_addr):
    mess, addr = mess_addr
    print(soc, mess_addr)
    time.sleep(1)
    mess = 'got this %s %s' %addr
    print('finash send!!')
    soc.sendto(mess.encode(), addr)



class TcpSocket():

    def __init__(self, l_addr=None, handle_func=print):
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if l_addr:
            if handle_func:
                self.server = server.StreamServer(l_addr, handle_func)
            else:
                self.soc.bind(l_addr)

    def conn(self, addr):
        self.soc.connect(addr)

    def send_message(self, message):
        self.soc.send(message.encode())

    def recv_handle(self, hadle_func=print):
        try:
            hadle_func(self.soc.recv(1024,))
        except Exception as err:
            print(err)


def server_handle_func(soc, address):
    data = soc.recv(1024)
    print(data, address)
    soc.send("Hello clinet!\n %".encode())
    return soc


# playground
def run_udp_send(message='handashuai 1234', l_port=10036, addr=('47.104.190.254', 10036)):
    udp_s = UdpSocket(('0.0.0.0', l_port), 4)
    udp_s.send_message(message, addr)
    udp_s.recv_handle()
    udp_s.recv_handle()
    udp_s.recv_handle()
    udp_s.soc.close()



def run_udp_listen(l_port=10036):
    udp_s = UdpSocket(('0.0.0.0', l_port))
    print('udp listening %s ....' % l_port)
    while True:
        data, addr = udp_s.soc.recvfrom(1024)
        print(data, addr)
        udp_s.soc.sendto('不要回答'.encode(), addr)
        udp_s.send_message('不要回答2', addr)


def run_tcp_server(l_port=10036):
    tcp_s = TcpSocket(('0.0.0.0', l_port), server_handle_func)
    print('tcp server listening %s .... ' % l_port)
    tcp_s.server.serve_forever()


def run_tcp_send(message='handashuai 1234', l_port=10036, addr=('47.104.190.254', 10036)):
    tcp_s = TcpSocket(('0.0.0.0', l_port), handle_func=None)  # handle_func=None 特殊用法 表示send型的TcpSocket
    tcp_s.conn(addr)
    tcp_s.soc.send(message.encode())
    print(tcp_s.soc.recv(1024))
    tcp_s.send_message(message)
    tcp_s.recv_handle()

    tcp_s.soc.close()


r_host = '119.139.198.170'
udp_s = UdpSocket(('0.0.0.0', 10038), 2)
import threading


def try_p2p_udpsend():
    spawn_list = [gevent.spawn(udp_s.send_message, 'handashuai 1234' + 'detect(%s,%s)' % (r_host, i), (r_host, i)) for i
                  in range(57000, 65535)]
    gevent.joinall(spawn_list)



if __name__ == "__main__":
    pass
    threading.Thread(target=udp_s.listen_bytimes, args=(10)).start()