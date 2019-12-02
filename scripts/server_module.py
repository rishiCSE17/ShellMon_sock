import socket
import time
import threading as th
import json
import os
import matplotlib.pyplot as plt
import drawnow

print_lock = th.Lock()
window = []
window_size = 20

plot_dict = {'none': []}

window = 3
host_ip = '127.0.0.1'
host_port = int(input(r'Enter the port number : '))
buffer_size = 15000

# where there are many sources you've to isolate data by their port numbers
data_dict = {}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', host_port))
s.listen(1)

data_arr = []
thread_list = []

'''
def  plotme():
    cpu=data_dict[k][-1]['cpu']['mean_load']
    mem=round(data_dict[k][-1]['mem']['util']
    net_i=data_dict[k][-1]['net']['Ingress_util']
    net_e=data_dict[k][-1]['net']['Egress_util']

    load= (float(cpu) + float(mem) + float(net_i) + float(net_e))/4
    #plt.plot()
'''


def receiver_loop(conn, addr):
    global data_dict
    global plt

    while True:
        data = conn.recv(buffer_size)
        os.system('clear')
        if not data:
            print('no data')
            data_dict.pop(addr[1])
            break
        # print('received data : ', data)

        with print_lock:
            data = json.loads(data)
            # addr is touple and port number in inedex 1
            if addr[1] not in list(data_dict.keys()):
                data_dict[addr[1]] = [data]
            else:
                if len(data_dict[addr[1]]) > window:
                    data_dict[addr[1]].pop(0)
                data_dict[addr[1]].append(data)

                # drawnow(plotme)

            for k in data_dict:
                cpu = data_dict[k][-1]['cpu']['mean_load']
                mem = data_dict[k][-1]['mem']['util']
                net_i = data_dict[k][-1]['net']['Ingress_util']
                net_e = data_dict[k][-1]['net']['Egress_util']

                load = (float(cpu) + float(mem) + float(net_i) + float(net_e)) / 4

                # plot_dict[k]
                # print(f'Source Port {k} : {data_dict[k][-1]}')
                print(f"======================================================")
                print(f"Client : {k}")
                print(f"-------------------------------------------------------")
                print(f"CPU load : {data_dict[k][-1]['cpu']['mean_load']}")
                print(f"Mem load : {data_dict[k][-1]['mem']['util']}")
                print(f"Net Ingr : {data_dict[k][-1]['net']['Ingress_util']}")
                print(f"Net Egrr : {data_dict[k][-1]['net']['Egress_util']}")
                print(f"-------------------------------------------------------")
                print(f"Cumulative load : {load}")
                print(f"-------------------------------------------------------")
            reply_data = 'Received'
            conn.send(str.encode(reply_data))


while True:
    print('Listening...')
    conn, addr = s.accept()
    print('Connection Address :', addr)
    t = th.Thread(target=receiver_loop, args=(conn, addr))
    t.start()
    thread_list.append(t)
    os.system('New Client Discovered... !')

    time.sleep(5)