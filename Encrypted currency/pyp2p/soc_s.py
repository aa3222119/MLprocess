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

network = '<broadcast>'

PORT = int(kargs['-p'])
s.sendto(kargs['-m'].encode('utf-8'), (network, PORT))