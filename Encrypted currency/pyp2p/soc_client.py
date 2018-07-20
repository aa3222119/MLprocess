'''客户端（UDP协议局域网广播）'''

import socket,getopt,sys

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

kargs = {'-m': 'Client broadcast message!', '-p': 10060}
try:
    opts, args = getopt.getopt(sys.argv[1:], "m:p:",)
    opts_dict = {x[0]: x[1] for x in opts}
    kargs.update(opts_dict)

except getopt.GetoptError as err:
    print(err)
PORT = int(kargs['-p'])
s.bind(('', PORT))
print('Listening for broadcast at ', s.getsockname())


while True:
    data, address = s.recvfrom(65535)
    print('Server received from {}:{}'.format(address, data.decode('utf-8')))