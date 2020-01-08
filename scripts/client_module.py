'''
sends data to the server

@author : Saptarshi Ghosh
test
'''

import happybase as hb
import socket
import time
import random
import fetch_util as util
import json

def hbase_conn(host, tab):
    conn=hb.Connection(host)
    return conn.table(tab)

def bytefy(d):
    ret={'cpu:vcore':str.encode(str(d['cpu']['count_vir'])),
         'cpu:pcore':str.encode(str(d['cpu']['count_phy'])),
         'cpu:freq':str.encode(str(d['cpu']['mean_freq'])),
         'cpu:load':str.encode(str(d['cpu']['mean_load'])),
         'mem:freq':str.encode(str(d['mem']['freq'])),
         'mem:vol':str.encode(str(d['mem']['vol'])),
         'mem:util':str.encode(str(d['mem']['util'])),
         'net:ing':str.encode(str(d['net']['Ingress_util'])),
         'net:egg':str.encode(str(d['net']['Egress_util'])),
         'net:speed':str.encode(str(d['net']['Speed']))}
    return ret

def insert_hbase(tab, data):
    tab.put(str(int(time.time())).encode(),bytefy(data))

def send_loop(client_port,
              host_ip,
              host_port,
              buffer_size=1024,
              cpu_interval=2,
              delay=1,
              mypass='',
              intf='eth0',
              is_wl=True,
              hbase=False,
              hbase_ip='',
              hbase_tab=''):
    print('================= TRANSMISSION INITIATED ==============')

    #initiate socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0',client_port))
    s.connect((host_ip, host_port))

    if hbase:
        print(f'Connecting {hbase_ip}...')
        htab = hbase_conn(hbase_ip, hbase_tab)

    while True:
        try:
            #msg=input('Enter a message : ')
            msg=util.main_fetch_util(loop=False,
                                     delay=delay,
                                     cpu_interval=cpu_interval,
                                     my_pass=mypass,
                                     intf=intf,
                                     is_wl=is_wl)

            time.sleep(3)

            if hbase:
                insert_hbase(tab=htab,data=msg)

            msg_byte=str.encode(json.dumps(msg))
            s.send(msg_byte)
            print(f'| sent     \t | {msg_byte} \t |')
            data = s.recv(buffer_size)
            print(f'| received \t | {data} \t |')
            print('------------------------------------------')
        except KeyboardInterrupt:
            s.close()

def main():
    client_port = int(input('Enter port number \t : '))
    host_ip = input('Enter Server IP \t : ')
    host_port = int(input('Enter Server Port \t : '))
    buffer_size = int(input('Enter Buffer size \t : '))
    client_password=input('Enter your password : ')
    intf=input('Enter interface to monitor \t : ')
    hbase=input('Using HBase Integration (y/n)? ')

    if hbase == 'y':
        hbase = True
        hbase_ip = input('Enter HBase Server IP \t : ')
        hbase_tab = input('Enter Target Table name \t : ')
    else:
        hbase = False

    while True:
        is_wl=input('is this a wireless interface ? (y/n) : \t')
        if is_wl == 'y':
            is_wl=True
            break
        elif is_wl == 'n':
            is_wl = False
            break
        else:
            continue

    send_loop(client_port=client_port,
              host_ip=host_ip,
              host_port=host_port,
              mypass=client_password,
              intf=intf,
              is_wl=is_wl,
              hbase=hbase,
              hbase_ip=hbase_ip,
              hbase_tab=hbase_tab)

main()