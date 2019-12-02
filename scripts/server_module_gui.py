import socket
import time
import threading as th
import json
import os
import matplotlib.pyplot as plt
from drawnow import  *

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

plot_data = {}
data_arr = []
thread_list = []
fig = plt.figure()
ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(223)
ax4 = fig.add_subplot(224)


def define_axis():
    global fig

    axis = []
    size = len(data_dict)
    for i in range(size*4):
        axis.append(fig.add_subplot(size,4,i+1))

    return axis

def _mov_avg(a1):
    ma1 = []   # moving average list
    avg1 = 0   # moving average pointwise
    count = 0
    for i in range(len(a1)):
        count += 1
        avg1 = ((count-1)*avg1+a1[i])/count
        ma1.append(round(avg1, 4))    # cumulative average formula
        # μ_n=((n-1) μ_(n-1)  + x_n)/n
    return ma1


def  plot_me():
    axes = define_axis()
    a_m = -4
    a_c = -3
    a_i = -2
    a_e = -1
    for k in plot_data:
        plotter(ax=axes[a_m+4], data=plot_data[k]['mem'], key=k, name='Memory', col='m')
        plotter(ax=axes[a_c + 4], data=plot_data[k]['cpu'], key=k, name='CPU', col='c')
        plotter(ax=axes[a_i + 4], data=plot_data[k]['net_i'], key=k, name='NetI', col='g')
        plotter(ax=axes[a_e + 4], data=plot_data[k]['net_e'], key=k, name='NetE', col='r')
    fig.suptitle('ShellMon Experiment')


def show_graphs():
    drawnow(plot_me)


def plotter(ax, data, key, name, col):
    ax.grid(True)
    ax.plot(list(range(len(_mov_avg(data)))), _mov_avg(data), linewidth=2, label='{} {}'.format(name, key), color=col)
    ax.set_ylabel('Moving {}'.format(name))
    ax.set_xlabel('Time (seconds)')
    ax.fill_between(list(range(len(_mov_avg(data)))), _mov_avg(data), 0, alpha=0.5, color=col)
    ax.legend()
    plt.subplot(ax)


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

                if k in plot_data:
                    plot_data[k]['cpu'].append(cpu)
                    plot_data[k]['mem'].append(cpu)
                    plot_data[k]['net_i'].append(net_i)
                    plot_data[k]['net_e'].append(net_e)
                else:
                    plot_data[k] = {'cpu': [cpu],
                                    'mem': [mem],
                                    'net_i': [net_i],
                                    'net_e': [net_e]}

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
            show_graphs()


while True:
    print('Listening...')
    conn, addr = s.accept()
    print('Connection Address :', addr)
    t = th.Thread(target=receiver_loop, args=(conn, addr))
    t.start()
    thread_list.append(t)
    os.system('New Client Discovered... !')

    time.sleep(5)